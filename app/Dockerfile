FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker build -t fastapi-service-docker-ci-cd-demo -f app/Dockerfile .
# docker run -d -p 8000:8000 fastapi-service-docker-ci-cd-demo