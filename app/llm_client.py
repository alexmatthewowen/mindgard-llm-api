import json
import os
import abc
import requests


class ForbiddenWordException(Exception):
    pass


class LLMClient(abc.ABC):
    @abc.abstractmethod
    def get_response(self, prompt: str) -> str:
        pass


class OllamaClient(LLMClient):
    def __init__(self, url, model):
        self.__url = url
        self.__model = model

    def get_response(self, prompt: str) -> str:
        payload = {
            "model": self.__model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.__url, json=payload)

        if response.status_code != 200:
            raise Exception('Ollama request failed.')

        return response.json().get("response", "")


class LLMResponseFirewallClient(LLMClient):
    """
    Wraps a LLMClient instance, acting as a "firewall" against forbidden words returned from the client.
    """
    def __init__(self, client: LLMClient, forbidden_words_json: str):
        self.__llm_client = client
        self.__forbidden_words_json = forbidden_words_json

    def get_response(self, prompt: str) -> str:
        response = self.__llm_client.get_response(prompt)

        with open(self.__forbidden_words_json) as words:
            words = json.load(words)
            if any(word.lower() in response.lower() for word in words['forbidden_words']): #Doesn't scale well, but works fine for short text and a short list of words
                raise ForbiddenWordException('Encountered a forbidden word in LLM response.')

        return response


def get_client() -> LLMClient:
    ollama_client = OllamaClient(
        os.getenv('OLLAMA_URL'),
        os.getenv('OLLAMA_MODEL')
    )

    return LLMResponseFirewallClient(
        ollama_client,
        os.getenv('FORBIDDEN_WORDS_JSON_FILE')
    )

llm_client = get_client()