ingestion:
	python3 ./vectordb/file_ingestion.py

up:
	docker-compose -f docker/docker-compose.yml up --build -d

down:
	docker-compose -f docker/docker-compose.yml down
