.PHONY: build run stop clean logs test

build:
	docker-compose build

run:
	docker-compose up -d

dev:
	docker-compose up

stop:
	docker-compose down

clean:
	docker-compose down -v --rmi all

logs:
	docker-compose logs -f

test:
	curl -f http://localhost:8000/health

restart:
	docker-compose restart

scale:
	docker-compose up --scale jobspy-api=3 -d

prod:
	docker-compose --profile production up -d

help:
	@echo "Available commands:"
	@echo "  build     - Build Docker images"
	@echo "  run       - Run in background"
	@echo "  dev       - Run in foreground with logs"
	@echo "  stop      - Stop all services"
	@echo "  clean     - Remove containers and images"
	@echo "  logs      - Show logs"
	@echo "  test      - Test health endpoint"
	@echo "  restart   - Restart services"
	@echo "  scale     - Scale to 3 instances"
	@echo "  prod      - Run with Nginx"
