#!/bin/sh

echo "Starting Ollama server..."
ollama serve &

echo "Waiting for Ollama to be ready..."
until curl -s http://localhost:11434/api/tags > /dev/null; do
  sleep 1
done

echo "Pulling model: llama3"
ollama pull llama3

echo "Model ready. Ollama is running."
tail -f /dev/null
