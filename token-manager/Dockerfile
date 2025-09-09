FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY token_manager.py .
COPY config.py .

CMD ["python", "token_manager.py"]
