import logging
from flask import Flask, jsonify, Response, request
from marshmallow import Schema, fields, ValidationError
from werkzeug.exceptions import HTTPException
from llm_client import ForbiddenWordException
from llm_client import llm_client

app = Flask(__name__)

class GenerateRequestSchema(Schema):
    prompt = fields.String(required=True)
    user_id = fields.String(required=True)

request_schema = GenerateRequestSchema()

@app.post('/generate')
def generate() -> tuple[Response, int]:
    """
    TODO: Authentication, access control
    """
    data = request.get_json()

    try:
        request_schema.load(data)
        response = llm_client.get_response(data.get('prompt'))
        return jsonify({'response': response}), 201
    except ForbiddenWordException:
        logging.warning('A user\'s prompt resulted in a forbidden word returned from the LLM.', {
            'user_id': data.get('user_id'),
            'prompt': data.get('prompt')
        })
        return jsonify({'error': 'The response from the LLM contained a forbidden word.'}), 422



@app.errorhandler(ValidationError)
def handle_validation_error(e) -> tuple[Response, int]:
    return jsonify({'error': e.messages}), 400


@app.errorhandler(Exception)
def handle_uncaught_error(e) -> tuple[Response, int]:
    if isinstance(e, HTTPException):
        return jsonify({
        'error': e.description
    }), e.code

    logging.error('An unhandled exception resulted in a 500 response.', {
        'error': e.description
    })

    return jsonify({
        'error': 'Oops! An error occurred, please try again later.'
    }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
