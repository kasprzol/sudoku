import sudoku


def test_logic_digit_groups_in_row_simple():
    # given_board = [
    #     [7, 2, 5, 6, 8, 1, 3, 4, 9],
    #     [8, 9, 4, 5, 7, 3, 2, 6, 1],
    #     [6, 1, 3, 9, 2, 4, 7, 8, 5],
    #     [1, 6, 9, 2, 4, 7, 8, 5, 3],
    #     [3, 7, 2, 8, 6, 5, 1, 9, 4],
    #     [4, 5, 8, 1, 3, 9, 6, 7, 2],
    #     [5, 3, 7, 4, 1, 8, 9, 2, 6],
    #     [9, 8, 6, 3, 5, 2, 4, 1, 7],
    #     [2, 4, 1, 7, 9, 6, 5, 3, 8],
    # ]
    given_board = [
        [[7], [2, 5], [2, 5], [2, 5, 6, 8], [5, 6, 8], [1], [3], [4], [9]],
    ]
    expected_board = [
        [[7], [2, 5], [2, 5], [6, 8], [6, 8], [1], [3], [4], [9]],
    ]
    sudoku.board = given_board
    sudoku.logic_same_digits_groups_in_row()
    assert sudoku.board == expected_board


def test_logic_digit_groups_in_row_complex():
    # given_board = [
    #     [7, 2, 5, 6, 8, 1, 3, 4, 9],
    #     [8, 9, 4, 5, 7, 3, 2, 6, 1],
    #     [6, 1, 3, 9, 2, 4, 7, 8, 5],
    #     [1, 6, 9, 2, 4, 7, 8, 5, 3],
    #     [3, 7, 2, 8, 6, 5, 1, 9, 4],
    #     [4, 5, 8, 1, 3, 9, 6, 7, 2],
    #     [5, 3, 7, 4, 1, 8, 9, 2, 6],
    #     [9, 8, 6, 3, 5, 2, 4, 1, 7],
    #     [2, 4, 1, 7, 9, 6, 5, 3, 8],
    # ]
    given_board = [
        [[1, 2, 5, 7], [1, 2, 4, 5], [1, 2, 4, 5], [1, 2, 4, 5, 6, 8], [1, 4, 5, 6, 8],
         [1, 2, 4, 5], [3], [1, 2, 4, 5], [9]],
    ]
    expected_board = [
        [[7], [1, 2, 4, 5], [1, 2, 4, 5], [6, 8], [6, 8], [1, 2, 4, 5], [3], [1, 2, 4, 5], [9]],
    ]
    sudoku.board = given_board
    sudoku.logic_same_digits_groups_in_row()
    assert sudoku.board == expected_board
