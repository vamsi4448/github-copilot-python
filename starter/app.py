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

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})

if __name__ == '__main__':
    app.run(debug=True)