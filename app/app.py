from flask import Flask, jsonify, Response, request
from werkzeug.exceptions import HTTPException

from llm_client import ForbiddenWordException
from llm_client import llm_client

app = Flask(__name__)

@app.post('/generate')
def generate() -> tuple[Response, int]:
    """
    TODO: Add some validation of the request parameters.
    TODO: Authentication, access control
    """
    data = request.get_json()

    try:
        response = llm_client.get_response(data.get("prompt"))
        return jsonify({"response": response}), 201
    except ForbiddenWordException:
        return jsonify({"error": "The response from the LLM contained a forbidden word."}), 422


@app.errorhandler(Exception)
def handle_uncaught_error(e) -> tuple[Response, int]:
    if isinstance(e, HTTPException):
        return jsonify({
        "error": e.description
    }), e.code

    return jsonify({
        "error": "Oops! An error occurred, please try again later."
    }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
