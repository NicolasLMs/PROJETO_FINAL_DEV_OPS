import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    app.config['TESTING'] = True
    # Sobrescreve a chave JWT para testes
    app.config['JWT_SECRET_KEY'] = 'test_secret_key'
    with app.test_client() as client:
        yield client

# Teste 1: Verificar a rota principal
def test_home_route(client):
    """Verifica se a rota / retorna 200 e a mensagem correta."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "API is running"}

# Teste 2: Verificar a rota /items
def test_get_items_route(client):
    """Verifica se a rota /items retorna 200 e uma lista."""
    response = client.get('/items')
    assert response.status_code == 200
    assert "items" in response.json
    assert isinstance(response.json["items"], list)

# Teste 3: Verificar a rota protegida (sem token)
def test_protected_route_no_token(client):
    """Verifica se a rota /protected retorna 401 sem um token JWT."""
    response = client.get('/protected')
    # 401 Unauthorized é o esperado
    assert response.status_code == 401
    assert "msg" in response.json
    assert response.json["msg"] == "Missing Authorization Header"