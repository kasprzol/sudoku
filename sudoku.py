__author__ = "Maciej 'kasprzol' Kasprzyk"

board = []
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


def logic():
    return logic_single_candidate()


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

def main():
    read_input()
    print_board()
    solve()
    if validate():
        print("\nA solution was found:")
        print_final_board()
    else:
        print("\nA solution could not been found :( :")
        print_board()



if __name__ == "__main__":
    main()
