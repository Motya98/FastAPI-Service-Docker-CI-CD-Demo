FROM python:3.11-slim
WORKDIR /file_handler
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /file_handler
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
