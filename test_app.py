import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test_secret_key'
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "API is running"}

def test_get_items_route(client):
    response = client.get('/items')
    assert response.status_code == 200
    assert "items" in response.json
    assert isinstance(response.json["items"], list)

def test_protected_route_no_token(client):
    response = client.get('/protected')
    assert response.status_code == 401
    assert "msg" in response.json
    assert response.json["msg"] == "Missing Authorization Header"