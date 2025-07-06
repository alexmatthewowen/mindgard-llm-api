import json
import os
import pytest
from unittest.mock import patch
from llm_client import LLMResponseFirewallClient, OllamaClient, ForbiddenWordException


#--------------------------------#
# Tests for OllamaClient         #
#--------------------------------#

def test_ollama_client_throws_exception_when_response_status_code_neq_200():
    ollama_client = OllamaClient('/test-url', 'llama3')

    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 404
        with pytest.raises(Exception):
            ollama_client.get_response('Is this going to throw an exception?')

def test_ollama_client_returns_expected_response():
    ollama_client = OllamaClient('/test-url', 'llama3')

    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'response': 'Nope, no exceptions here.'}
        ollama_client.get_response('Is this going to throw an exception?')

#--------------------------------------#
# Tests for LLMResponseFirewallClient  #
#--------------------------------------#

@pytest.fixture
def forbidden_words():
    with open(os.getenv('FORBIDDEN_WORDS_JSON_FILE')) as words:
        yield json.load(words)['forbidden_words']

def test_exception_thrown_when_forbidden_word_present_in_response(mocker, forbidden_words):
    mock_llm_client = mocker.Mock()

    for forbidden_word in forbidden_words:
        mock_llm_client.get_response.return_value = f"Your forbidden word is {forbidden_word}."
        client = LLMResponseFirewallClient(mock_llm_client, os.getenv('FORBIDDEN_WORDS_JSON_FILE'))

        with pytest.raises(ForbiddenWordException):
            client.get_response('What is my forbidden word?')

def test_response_returned_successfully(mocker):
    expected_response = 'No forbidden words here!'
    mock_llm_client = mocker.Mock()
    mock_llm_client.get_response.return_value = expected_response
    client = LLMResponseFirewallClient(mock_llm_client, os.getenv('FORBIDDEN_WORDS_JSON_FILE'))

    assert expected_response == client.get_response('Any forbidden words?')


