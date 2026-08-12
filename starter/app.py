from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty')
    clues_param = request.args.get('clues')

    if difficulty:
        try:
            clues = sudoku_logic.get_clues_for_difficulty(difficulty)
        except ValueError:
            clues = sudoku_logic.DIFFICULTY_LEVELS[sudoku_logic.DEFAULT_DIFFICULTY]
    elif clues_param is not None:
        try:
            clues = int(clues_param)
        except ValueError:
            clues = sudoku_logic.DIFFICULTY_LEVELS[sudoku_logic.DEFAULT_DIFFICULTY]
    else:
        clues = sudoku_logic.DIFFICULTY_LEVELS[sudoku_logic.DEFAULT_DIFFICULTY]

    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle})

@app.route('/hint', methods=['POST'])
def get_hint():
    data = request.json or {}
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    if not board or len(board) != sudoku_logic.SIZE or any(len(row) != sudoku_logic.SIZE for row in board):
        return jsonify({'error': 'Invalid board'}), 400
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] == sudoku_logic.EMPTY:
                return jsonify({'row': i, 'col': j, 'value': solution[i][j]})
    return jsonify({'error': 'No empty cells available'}), 400

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    complete = True
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            value = board[i][j]
            if value == sudoku_logic.EMPTY:
                complete = False
                continue
            if value != solution[i][j]:
                incorrect.append([i, j])
                complete = False
    return jsonify({'incorrect': incorrect, 'complete': complete})

if __name__ == '__main__':
    app.run(debug=True)