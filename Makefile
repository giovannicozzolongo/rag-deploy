.PHONY: ingest serve eval test lint docker

ingest:
	python -m src.ingestion.run

serve:
	uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

eval:
	python -m evaluation.evaluate

test:
	pytest tests/ -v

lint:
	ruff check src/
	ruff format --check src/

docker:
	docker compose -f docker/docker-compose.yml up --build
