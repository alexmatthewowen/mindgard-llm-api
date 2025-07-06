import pytest
from unittest.mock import patch
from app import app
from llm_client import ForbiddenWordException, LLMResponseFirewallClient

headers = {
    'Content-Type': 'application/json'
}

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_success(client):
    expected_response = 'Fine thanks, how are you?'
    with patch('llm_client.LLMResponseFirewallClient.get_response') as mock_method:
        mock_method.return_value = expected_response
        json = {
            'user_id': 'user-123',
            'prompt': 'Hi, how are you?'
        }

        response = client.post('/generate', headers=headers, json=json)

        assert response.status_code == 201
        assert response.get_json() == {
            'response': 'Fine thanks, how are you?'
        }

def test_on_forbidden_word_found(client):
    with patch('llm_client.LLMResponseFirewallClient.get_response', side_effect=ForbiddenWordException('Forbidden word discovered')):
        json = {
            'user_id': 'user-123',
            'prompt': 'Hi, how are you?'
        }
        response = client.post('/generate', headers=headers, json=json)
        assert response.status_code == 422
        assert response.get_json() == {
            'error': 'The response from the LLM contained a forbidden word.'
        }

def test_400_returned_when_user_id_missing(client):
    json = {
        'prompt': 'Hi, how are you?'
    }
    response = client.post('/generate', headers=headers, json=json)
    assert response.status_code == 400


def test_400_returned_when_prompt_missing(client):
    json = {
        'user_id': 'user-123',
    }
    response = client.post('/generate', headers=headers, json=json)
    assert response.status_code == 400

#TODO Add test coverage for error handler