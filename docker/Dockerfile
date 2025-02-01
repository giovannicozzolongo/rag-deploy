FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY evaluation/ evaluation/
COPY data/ data/
COPY Makefile .

# build the index at image build time if docs are present
RUN python -m src.ingestion.run || echo "index build skipped (no docs)"

EXPOSE 8000 8501

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
