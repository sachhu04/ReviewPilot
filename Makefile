.PHONY: help build up down logs db-shell migrate status

# Default target
help:
	@echo "ReviewPilot Enterprise Deployment Commands"
	@echo ""
	@echo "Usage:"
	@echo "  make build      - Build all Docker images"
	@echo "  make up         - Start all services in the background"
	@echo "  make down       - Stop all services and remove containers"
	@echo "  make logs       - View logs from all services"
	@echo "  make db-shell   - Access PostgreSQL shell"
	@echo "  make migrate    - Run database migrations"
	@echo "  make status     - View status of all running containers"

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

db-shell:
	docker exec -it reviewpilot-db psql -U reviewpilot -d reviewpilot_db

migrate:
	docker exec -t reviewpilot-backend alembic upgrade head

status:
	docker compose ps
