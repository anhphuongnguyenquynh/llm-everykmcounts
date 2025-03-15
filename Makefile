ingestion:
	python3 ./vectordb/file_ingestion.py

up:
	docker-compose up --build -d

down:
	docker-compose down
