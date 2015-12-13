__author__ = "Maciej 'kasprzol' Kasprzyk"

from copy import copy, deepcopy

# "Drugs^W Globals are bad, m'kay. You shouldn't do globals. If you do them,
# you're bad, because globals are bad, m'kay. It's a bad thing to do globals, so
# don't be bad by doing globals, m'kay, that'd be bad. Globals are bad."
board = []
board_state_stack = []
solutions = []


class ValidationError(Exception):
    pass


def coordinates_to_square(row, col):
    return 3 * (row // 3) + col // 3


def square_to_row(square_num):
    return 3 * (square_num // 3)


def square_to_col(square_num):
    return 3 * (square_num % 3)


def read_input():
    with open("sudoku.in", "rt") as f:
        for input_line in f:
            line = []
            for char in input_line:
                if char in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    line.append([int(char)])
                elif char == '.':
                    line.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
                else:
                    print("Unknown char: %s" % ord(char))
            board.append(line)


def propagate_single_digit_in_cel(row, col):
    changes = False
    number_to_remove = board[row][col][0]
    for r in range(0, 9):
        if r != row and number_to_remove in board[r][col]:
            board[r][col].remove(number_to_remove)
            if len(board[r][col]) == 0:
                raise ValidationError()
            changes = True
    for c in range(0, 9):
        if c != col and number_to_remove in board[row][c]:
            board[row][c].remove(number_to_remove)
            if len(board[row][c]) == 0:
                raise ValidationError()
            changes = True
    square_num = coordinates_to_square(row, col)
    row_in_square_start = square_to_row(square_num)
    for r in range(row_in_square_start, row_in_square_start + 3):
        col_in_square_start = square_to_col(square_num)
        for c in range(col_in_square_start, col_in_square_start + 3):
            if r != row and c != col and number_to_remove in board[r][c]:
                board[r][c].remove(number_to_remove)
                if len(board[r][c]) == 0:
                    raise ValidationError()
                changes = True
    return changes


def propagate_constraints():
    changed = False
    for row in range(0, len(board)):
        for col in range(0, len(board[0])):
            if len(board[row][col]) == 1:
                if propagate_single_digit_in_cel(row, col):
                    print('Propagating single digit {d} from cell [{r}, {c}]'
                          .format(d=board[row][col][0], r=row+1, c=col+1))
                    print_board()
                    changed = True
    return changed


def logic_single_candidate_square():
    # for each square: if only one candidate for a given number in each square
    # then it must be that number (disregard other candidates in that square)
    changed = False
    for square in range(9):
        row_in_square_start = square_to_row(square)
        col_in_square_start = square_to_col(square)
        candidates_found = {x: [0, []] for x in range(1,10)}
        for r in range(row_in_square_start, row_in_square_start + 3):
            for c in range(col_in_square_start, col_in_square_start + 3):
                for candidate in board[r][c]:
                    candidates_found[candidate][0] += 1
                    candidates_found[candidate][1].append((r, c))
        if logic_single_candidate_2nd_stage(candidates_found,
                                            'square %s' % (square + 1)):
            changed = True
    return changed


def logic_single_candidate_2nd_stage(candidates_found, searching_in):
    changed = False
    for candidate in candidates_found:
        if candidates_found[candidate][0] == 1:
            r, c = candidates_found[candidate][1][0]
            # remove all other candidates from this cell
            # if it's not already a single candidate
            if len(board[r][c]) > 1:
                print('Found single candidate for number {d} in {thing} at '
                      '[{r}, {c}]'.format(d=candidate, thing=searching_in,
                                          r=r+1, c=c+1))
                board[r][c] = [candidate]
                changed = True
    return changed


def logic_single_candidate_row():
    # for each row: if only one candidate for a given number in a row
    # then it must be that number (disregard other candidates in that square)
    changed = False
    for r in range(len(board)):
        candidates_found = {x: [0, []] for x in range(1,10)}
        for c in range(len(board[0])):
            for candidate in board[r][c]:
                candidates_found[candidate][0] += 1
                candidates_found[candidate][1].append((r, c))
        if logic_single_candidate_2nd_stage(candidates_found,
                                            'row %s' % (r + 1)):
            changed = True
    return changed


def logic_single_candidate_columnn():
    # for each column: if only one candidate for a given number in a column
    # then it must be that number (disregard other candidates in that square)
    changed = False
    for c in range(len(board[0])):
        candidates_found = {x: [0, []] for x in range(1,10)}
        for r in range(len(board)):
            for candidate in board[r][c]:
                candidates_found[candidate][0] += 1
                candidates_found[candidate][1].append((r, c))
        if logic_single_candidate_2nd_stage(candidates_found,
                                            'column %s' % (c + 1)):
            changed = True
    return changed


def logic_single_candidate():
    if logic_single_candidate_square():
        return True
    if logic_single_candidate_row():
        return True
    if logic_single_candidate_columnn():
        return True
    return False


def logic_row_candidates_in_square():
    """
    This function checks if a specific digit candidates for a row are all in one
    square. This means that all other candidates for this digit in this square
    are impossible and can be removed.

    For example: given fallowing row of candidates grouped by their squares:
    [129][134][179] [245][378][689] [567][567][678]
    The candidates for digit 1 are all in the first square. So the digit for
    that row must be in that square and all other candidates for digit 1 in the
    first square can be eliminated.
    """
    changed = False
    for r in range(len(board)):
        digits_found_in_square = {d: set() for d in range(1, 10)}
        for c in range(len(board[0])):
            for candidate in board[r][c]:
                digits_found_in_square[candidate].add(coordinates_to_square(
                    r, c))
        for digit in digits_found_in_square:
            if len(digits_found_in_square[digit]) == 1:
                square = digits_found_in_square[digit].pop()
                # remove all candidates `digit` from `square` that are not on
                # row `r`
                row_start = square_to_row(square)
                col_start = square_to_col(square)
                for x in range(row_start, row_start + 3):
                    if x == r:
                        continue
                    for y in range(col_start, col_start + 3):
                        if digit in board[x][y]:
                            changed = True
                            board[x][y].remove(digit)
                            if len(board[x][y]) == 0:
                                raise ValidationError()
                if changed:
                    print("Removing candidates for number {d} in square "
                        "{square} that aren't on row {r}".format(
                            d=digit,square=square+1, r=r+1))
                    return changed
    return changed


def logic_column_candidates_in_square():
    """
    The same logic as in `logic_row_candidates_in_square` but for columns
    """
    changed = False
    for c in range(len(board[0])):
        digits_found_in_square = {d: set() for d in range(1, 10)}
        for r in range(len(board)):
            for candidate in board[r][c]:
                digits_found_in_square[candidate].add(coordinates_to_square(
                    r, c))
        for digit in digits_found_in_square:
            if len(digits_found_in_square[digit]) == 1:
                square = digits_found_in_square[digit].pop()
                # remove all candidates `digit` from `square` that are not on
                # column `c`
                row_start = square_to_row(square)
                col_start = square_to_col(square)
                for y in range(col_start, col_start + 3):
                    if y == c:
                        continue
                    for x in range(row_start, row_start + 3):
                        if digit in board[x][y]:
                            changed = True
                            board[x][y].remove(digit)
                            if len(board[x][y]) == 0:
                                raise ValidationError()
                if changed:
                    print("Removing candidates for number {d} in square "
                        "{square} that aren't on column {c}".format(
                            d=digit, square=square+1, c=c+1))
                    return changed
    return changed


def logic():
    if logic_single_candidate():
        print_board()
        return True
    if logic_row_candidates_in_square():
        print_board()
        return True
    if logic_column_candidates_in_square():
        print_board()
        return True
    return False


def bruteforce_solve():
    for r in range(len(board)):
        for c in range(len(board[0])):
            # there is more than 1 candidate, try them all
            if len(board[r][c]) > 1:
                cell = copy(board[r][c])
                for candidate in cell:
                    global board
                    board_state_stack.append(deepcopy(board))
                    board[r][c] = [candidate]
                    try:
                        solve()
                        if validate():
                            existing_solution = False
                            for s in solutions:
                                if equal_boards(board, s):
                                    existing_solution = True
                                    break
                            if not existing_solution:
                                solutions.append(deepcopy(board))
                                print_final_board()
                    except ValidationError:
                        pass
                    finally:
                        board = board_state_stack.pop()
    return False


def solve():
    changed = True
    while changed:
        changed = False
        if propagate_constraints():
            changed = True
            continue
        if logic():
            changed = True
            continue
    if not validate():
        bruteforce_solve()


def print_board():
    row_num = 1
    for row in board:
        print('%s: ' % row_num, end='')
        row_num += 1
        for cell in row:
            digits = []
            for candidate in range(1, 10):
                digits.append(str(candidate) if candidate in cell else ' ')
            print('[%s]' % ''.join(digits), end='')
        print('')
    print('')


def print_final_board():
    row_num = 1
    for row in board:
        print('%s: ' % row_num, end='')
        row_num += 1
        cells = [str(cell[0]) for cell in row]
        print('%s' % ''.join(cells))
    print('')


def validate():
    """Check if the puzzle was solved (only 1 candidate in each cell)"""
    for row in board:
        for cell in row:
            if len(cell) != 1:
                return False
    return True


def equal_boards(board1, board2):
    for r in range(len(board1)):
        for c in range(len(board1[0])):
            if board1[r][c] != board2[r][c]:
                return False
    return True


def main():
    read_input()
    print_board()
    solve()
    if len(solutions) > 0:
        print("\nA solution were found:")
        while len(solutions) > 0:
            global board
            board = solutions.pop()
            print_final_board()
    else:
        print("\nA solution could not been found :( :")
        print_board()


if __name__ == "__main__":
    main()
