FROM ollama/ollama:latest
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY start.sh /start.sh
RUN chmod +x ./start.sh
ENTRYPOINT ["/bin/sh"]
CMD ["./start.sh"]