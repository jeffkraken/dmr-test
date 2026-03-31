FROM python:3.10-slim

WORKDIR /app

RUN pip install transformers torch fastapi uvicorn

COPY server.py .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
