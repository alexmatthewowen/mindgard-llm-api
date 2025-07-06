# Flask LLM API

A simple Flask API that uses a service object to communicate with a local Ollama instance.

## Building and running the app

You can run the application by first installing Docker and then running `docker-compose up`. IMPORTANT: You will need to wait for the tinyllama model to be pulled into the container before you can get a response from the model.

To send a request to the API, you can use curl (or Postman) to hit the endpoint `http://127.0.0.1:5000/generate` with a POST request. Here is an example:

```
curl -X POST http://127.0.0.1:5000/generate -d '{"user_id": "user-123", "prompt": "What is notarize fraud?"}' -H "Content-Type: application/json"
```

You must supply a `user_id` field, and a `prompt` field, both of which must be strings. Also note the `Content-Type` header must be provided with a value of `application/json`.

## Running the tests

You can run the tests in the docker container by running `docker-compose exec app pytest`.
