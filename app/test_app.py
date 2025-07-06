import pytest
from unittest.mock import patch
from app import app
from llm_client import ForbiddenWordException, LLMResponseFirewallClient


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_success(client):
    expected_response = 'Fine thanks, how are you?'
    with patch('llm_client.LLMResponseFirewallClient.get_response') as mock_method:
        mock_method.return_value = expected_response
        json = {
            'prompt': 'Hi, how are you?'
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = client.post('/generate', headers=headers, json=json)

        assert response.status_code == 201
        assert response.get_json() == {
            'response': 'Fine thanks, how are you?'
        }

def test_on_forbidden_word_found(client):
    with patch('llm_client.LLMResponseFirewallClient.get_response', side_effect=ForbiddenWordException('Forbidden word discovered')):
        json = {
            'prompt': 'Hi, how are you?'
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = client.post('/generate', headers=headers, json=json)
        assert response.status_code == 422
        assert response.get_json() == {
            'error': 'The response from the LLM contained a forbidden word.'
        }

#TODO Add test coverage for error handler