import pytest

import app as app_module
from app import CURRENT, app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_game_state():
    CURRENT.clear()
    app_module.CURRENT.clear()
    yield
    CURRENT.clear()
    app_module.CURRENT.clear()
