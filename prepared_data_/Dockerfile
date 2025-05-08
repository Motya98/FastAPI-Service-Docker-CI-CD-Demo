FROM python:3.11-slim
WORKDIR /prepared_data_
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /prepared_data_
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
