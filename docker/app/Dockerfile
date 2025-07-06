FROM python:latest
WORKDIR /app
COPY app/ /app
COPY requirements.txt .
COPY .env .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
