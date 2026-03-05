# Makefile for Django + Docker project

.PHONY: help dev prod build-dev build-prod migrate makemigrations shell createsuperuser collectstatic down clean

help:
	@echo "Available targets:"
	@echo "  dev                Run dev server with Docker Compose (live reload)"
	@echo "  prod               Run production server (Gunicorn + Nginx)"
	@echo "  build-dev          Build dev Docker image"
	@echo "  build-prod         Build prod Docker image"
	@echo "  migrate            Run migrations (dev)"
	@echo "  makemigrations     Make migrations (dev)"
	@echo "  shell              Django shell (dev)"
	@echo "  createsuperuser    Create Django superuser (dev)"
	@echo "  collectstatic      Collect static files (prod)"
	@echo "  down               Stop all containers (dev/prod)"
	@echo "  clean              Remove __pycache__, *.pyc, *.sqlite3, media, static, vol, etc."

# Development

dev:
	docker compose -f docker-compose.dev.yml --env-file .env.dev up --build

build-dev:
	docker compose -f docker-compose.dev.yml --env-file .env.dev build

migrate:
	docker compose -f docker-compose.dev.yml --env-file .env.dev exec web python manage.py migrate

makemigrations:
	docker compose -f docker-compose.dev.yml --env-file .env.dev exec web python manage.py makemigrations

shell:
	docker compose -f docker-compose.dev.yml --env-file .env.dev exec web python manage.py shell

createsuperuser:
	docker compose -f docker-compose.dev.yml --env-file .env.dev exec web python manage.py createsuperuser

# Production

prod:
	docker compose -f docker-compose.prod.yml --env-file .env.prod up --build

build-prod:
	docker compose -f docker-compose.prod.yml --env-file .env.prod build

collectstatic:
	docker compose -f docker-compose.prod.yml --env-file .env.prod exec web python manage.py collectstatic --noinput

# Common

down:
	docker compose -f docker-compose.dev.yml down || true
	docker compose -f docker-compose.prod.yml down || true

clean:
	rm -rf __pycache__ */__pycache__ *.pyc *.pyo *.sqlite3 *.db media/ static/ vol/