import pytest
from app import app  # Importa a sua instância 'app' do Flask

@pytest.fixture
def client():
    """
    Cria e configura um cliente de teste para cada teste.
    Isso é um 'fixture' do pytest.
    """
    # Coloca o app em modo de teste
    app.config['TESTING'] = True
    
    # Define uma chave secreta para o ambiente de teste
    app.config['JWT_SECRET_KEY'] = 'test_secret_key'

    # 'app.test_client()' cria um cliente virtual para fazer requisições
    with app.test_client() as client:
        # 'yield' entrega o cliente para a função de teste
        yield client

# --- Testes das Rotas ---
# O Pytest vai procurar e rodar todas as funções
# que começam com 'test_'

def test_home_route(client):
    """Testa a rota principal '/'."""
    response = client.get('/')
    
    assert response.status_code == 200
    assert response.json == {"message": "API is running"}

def test_get_items_route(client):
    """Testa a rota '/items'."""
    response = client.get('/items')
    
    assert response.status_code == 200
    assert response.json == {"items": ["item1", "item2", "item3"]}

def test_swagger_ui_route(client):
    """Testa se a rota do Swagger UI carrega."""
    response = client.get('/swagger')
    
    assert response.status_code == 200
    # Verifica se o HTML contém a palavra "Swagger"
    assert b"Swagger UI" in response.data

# --- Testes das Rotas com JWT (Autenticação) ---

def test_login_route(client):
    """Testa a rota de login '/login'."""
    response = client.post('/login')
    
    assert response.status_code == 200
    # Verifica se a resposta JSON contém a chave 'access_token'
    assert 'access_token' in response.json

def test_protected_route_no_token(client):
    """Testa a rota '/protected' SEM um token de acesso."""
    response = client.get('/protected')
    
    # Deve retornar 401 (Unauthorized)
    assert response.status_code == 401
    assert response.json == {"msg": "Missing Authorization Header"}

def test_protected_route_with_token(client):
    """Testa a rota '/protected' COM um token de acesso válido."""
    
    # 1. Primeiro, fazemos login para obter um token
    login_response = client.post('/login')
    assert login_response.status_code == 200
    token = login_response.json['access_token']

    # 2. Preparamos o cabeçalho (header) de autorização
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # 3. Fazemos a requisição para a rota protegida usando o token
    protected_response = client.get('/protected', headers=headers)
    
    assert protected_response.status_code == 200
    assert protected_response.json == {"message": "Protected route"}