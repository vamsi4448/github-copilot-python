import sudoku_logic


def assert_valid_completed_board(board):
    for row in board:
        assert set(row) == set(range(1, 10))

    for col_index in range(sudoku_logic.SIZE):
        column = [board[row_index][col_index] for row_index in range(sudoku_logic.SIZE)]
        assert set(column) == set(range(1, 10))

    for start_row in (0, 3, 6):
        for start_col in (0, 3, 6):
            block = [
                board[row][col]
                for row in range(start_row, start_row + 3)
                for col in range(start_col, start_col + 3)
            ]
            assert set(block) == set(range(1, 10))


def test_create_empty_board_returns_9_by_9_zero_grid():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_is_safe_allows_valid_placement():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.is_safe(board, 0, 0, 5) is True
    assert sudoku_logic.is_safe(board, 0, 1, 1) is True


def test_is_safe_rejects_duplicate_in_row_column_and_box():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 5
    board[0][1] = 6
    board[1][0] = 7
    board[0][2] = 8

    assert sudoku_logic.is_safe(board, 0, 1, 5) is False
    assert sudoku_logic.is_safe(board, 1, 0, 5) is False

    board = sudoku_logic.create_empty_board()
    board[0][0] = 1
    board[0][1] = 2
    board[0][2] = 3
    board[1][0] = 4
    board[1][1] = 5
    board[2][0] = 7
    board[1][2] = 8
    board[2][1] = 9

    assert sudoku_logic.is_safe(board, 2, 2, 1) is False


def test_fill_board_solves_empty_board():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.fill_board(board) is True
    assert_valid_completed_board(board)


def test_generate_puzzle_returns_valid_puzzle_and_solution():
    clues = 35
    puzzle, solution = sudoku_logic.generate_puzzle(clues)

    assert len(puzzle) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert len(solution) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in solution)

    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == clues
    assert sum(cell != sudoku_logic.EMPTY for row in solution for cell in row) == 81
    assert puzzle != solution
    assert_valid_completed_board(solution)
