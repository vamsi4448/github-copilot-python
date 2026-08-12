import sudoku_logic

from app import CURRENT, app


def test_index_route_returns_html(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.content_type.startswith('text/html')
    text = response.get_data(as_text=True)
    assert 'id="timer"' in text
    assert 'id="elapsed-time"' in text
    assert 'id="theme-toggle"' in text
    assert 'Top 10 Fastest Times' in text
    assert 'id="scoreboard-body"' in text


def test_new_game_route_returns_puzzle_and_stores_solution(client):
    response = client.get('/new?clues=35')

    assert response.status_code == 200
    payload = response.get_json()
    assert 'puzzle' in payload
    assert len(payload['puzzle']) == 9
    assert all(len(row) == 9 for row in payload['puzzle'])
    assert sum(cell != 0 for row in payload['puzzle'] for cell in row) == 35
    assert CURRENT['solution'] is not None
    assert len(CURRENT['solution']) == 9


def test_new_game_route_respects_difficulty_levels(client):
    difficulties = {
        'easy': 45,
        'medium': 35,
        'hard': 28,
    }

    for difficulty, expected_clues in difficulties.items():
        response = client.get(f'/new?difficulty={difficulty}')
        assert response.status_code == 200
        payload = response.get_json()
        assert sum(cell != 0 for row in payload['puzzle'] for cell in row) == expected_clues
        assert CURRENT['solution'] is not None
        assert sudoku_logic.count_solutions(payload['puzzle'], limit=2) == 1


def test_check_solution_route_reports_incorrect_cells(client):
    client.get('/new?clues=35')
    solution = [row[:] for row in CURRENT['solution']]

    if solution[0][0] != 9:
        solution[0][0] = 9
    else:
        solution[0][0] = 8

    response = client.post('/check', json={'board': solution})

    assert response.status_code == 200
    payload = response.get_json()
    assert [0, 0] in payload['incorrect']
    assert payload['incorrect']


def test_check_solution_route_reports_complete_when_board_is_correct(client):
    client.get('/new?clues=35')
    response = client.post('/check', json={'board': CURRENT['solution']})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload['incorrect'] == []
    assert payload['complete'] is True


def test_check_solution_route_reports_incomplete_when_empty_cells_remain(client):
    client.get('/new?clues=35')
    board = [row[:] for row in CURRENT['solution']]
    board[0][0] = 0

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload['incorrect'] == []
    assert payload['complete'] is False


def test_hint_route_returns_one_empty_cell(client):
    client.get('/new?clues=35')
    puzzle = CURRENT['puzzle']
    board = [row[:] for row in puzzle]

    response = client.post('/hint', json={'board': board})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload['row'] is not None
    assert payload['col'] is not None
    assert payload['value'] == CURRENT['solution'][payload['row']][payload['col']]
    assert board[payload['row']][payload['col']] == 0


def test_hint_route_respects_player_entries(client):
    client.get('/new?clues=35')
    puzzle = CURRENT['puzzle']
    board = [row[:] for row in puzzle]

    # fill one empty cell with a player-entered value and leave another empty
    empty_cells = [(i, j) for i in range(9) for j in range(9) if board[i][j] == 0]
    assert empty_cells
    player_row, player_col = empty_cells[0]
    board[player_row][player_col] = 1

    response = client.post('/hint', json={'board': board})
    assert response.status_code == 200
    payload = response.get_json()
    assert [payload['row'], payload['col']] != [player_row, player_col]
    assert payload['value'] == CURRENT['solution'][payload['row']][payload['col']]


def test_hint_without_game_returns_400(client):
    response = client.post('/hint', json={'board': [[0 for _ in range(9)] for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_check_solution_without_game_returns_400(client):
    response = client.post('/check', json={'board': [[0 for _ in range(9)] for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}
