import copy
import random

SIZE = 9
EMPTY = 0
DEFAULT_DIFFICULTY = 'medium'
DIFFICULTY_LEVELS = {
    'easy': 45,
    'medium': 35,
    'hard': 28,
}

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def find_empty_cell(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                return row, col
    return None


def count_solutions(board, limit=2):
    working = deep_copy(board)
    solution_count = 0

    def search():
        nonlocal solution_count
        if solution_count >= limit:
            return

        empty_cell = find_empty_cell(working)
        if empty_cell is None:
            solution_count += 1
            return

        row, col = empty_cell
        for num in range(1, SIZE + 1):
            if not is_safe(working, row, col, num):
                continue
            working[row][col] = num
            search()
            if solution_count >= limit:
                working[row][col] = EMPTY
                return
            working[row][col] = EMPTY

    search()
    return solution_count


def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


def remove_cells(board, clues):
    attempts = SIZE * SIZE - clues
    while attempts > 0:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        if board[row][col] != EMPTY:
            board[row][col] = EMPTY
            attempts -= 1


def generate_puzzle(clues=35):
    max_attempts = 200

    for _ in range(max_attempts):
        board = create_empty_board()
        fill_board(board)
        solution = deep_copy(board)
        puzzle = deep_copy(board)

        positions = [(row, col) for row in range(SIZE) for col in range(SIZE)]
        random.shuffle(positions)

        for row, col in positions:
            if sum(cell != EMPTY for line in puzzle for cell in line) <= clues:
                break
            value = puzzle[row][col]
            puzzle[row][col] = EMPTY
            if count_solutions(puzzle, limit=2) != 1:
                puzzle[row][col] = value

        if sum(cell != EMPTY for line in puzzle for cell in line) == clues and count_solutions(puzzle, limit=2) == 1:
            return puzzle, solution

    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    puzzle = deep_copy(board)
    positions = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(positions)

    for row, col in positions:
        if sum(cell != EMPTY for line in puzzle for cell in line) <= clues:
            break
        value = puzzle[row][col]
        puzzle[row][col] = EMPTY
        if count_solutions(puzzle, limit=2) != 1:
            puzzle[row][col] = value

    return puzzle, solution


def get_clues_for_difficulty(difficulty):
    if not isinstance(difficulty, str):
        raise ValueError('Difficulty must be a string')

    difficulty_key = difficulty.lower().strip()
    if difficulty_key not in DIFFICULTY_LEVELS:
        raise ValueError(f'Unknown difficulty {difficulty!r}')

    return DIFFICULTY_LEVELS[difficulty_key]
