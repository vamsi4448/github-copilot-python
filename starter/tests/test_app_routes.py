from app import CURRENT, app


def test_index_route_returns_html(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.content_type.startswith('text/html')


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


def test_check_solution_without_game_returns_400(client):
    response = client.post('/check', json={'board': [[0 for _ in range(9)] for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}
