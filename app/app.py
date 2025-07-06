import requests
from flask import Flask, jsonify, Response

app = Flask(__name__)

@app.get('/generate')
def conversation() -> tuple[Response, int]:
    payload = {
        "model": 'llama3',
        "prompt": 'Hello, how are you?',
        "stream": False
    }

    try:
        response = requests.post('http://ollama:11434/api/generate', json=payload)
        response.raise_for_status()
        llm_response = response.json().get("response", "")
        return jsonify({"response": llm_response}), 201
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
