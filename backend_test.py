import pytest
from app import app, db, ChatHistory
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database to avoid affecting the actual database
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create test database tables
        yield client
        with app.app_context():
            db.drop_all()  # Drop test database tables after tests are complete

def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "index.html" in response.data.decode()

@patch('app.openai.ChatCompletion.create')  # Mock the response from OpenAI API
def test_api_route(mock_openai, client):
    mock_response = {'choices': [{'message': {'content': 'Test response'}}]}
    mock_openai.return_value = mock_response

    response = client.post('/api', json={'message': 'Hello'})
    assert response.status_code == 200
    assert response.data.decode() == 'Test response'

    # Test if the database correctly stored the data
    with app.app_context():
        chat_entry = ChatHistory.query.first()
        assert chat_entry.user_message == 'Hello'
        assert chat_entry.ai_response == 'Test response'
