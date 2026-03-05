# Django + Dockerized Project

## Local Development (with Docker Compose)

1. Copy `.env.dev.example` to `.env.dev` and set your own `SECRET_KEY`.
2. Build and start the dev server:

	 ```sh
	 docker compose -f docker-compose.dev.yml --env-file .env.dev up --build
	 ```

	 - Code changes are live-reloaded (volumes mounted).
	 - Access at [http://localhost:8000/](http://localhost:8000/)

3. To run migrations manually:

	 ```sh
	 docker compose -f docker-compose.dev.yml exec web python manage.py migrate
	 ```

## Production (Gunicorn + Nginx)

1. Copy `.env.prod.example` to `.env.prod` and set your own `SECRET_KEY`, `ALLOWED_HOSTS`, etc.
2. Build and start the production stack:

	 ```sh
	 docker compose -f docker-compose.prod.yml --env-file .env.prod up --build
	 ```

	 - Nginx serves static files from `/vol/static` and media from `/vol/media`.
	 - Gunicorn runs Django app on port 8000, proxied by Nginx on port 80.
	 - Entrypoint script runs migrations and collectstatic automatically.

3. To run management commands in the web container:

	 ```sh
	 docker compose -f docker-compose.prod.yml exec web python manage.py <command>
	 ```

## Project Structure

- `config/settings/` — Split settings: `base.py`, `dev.py`, `prod.py`
- `static/` — For future static assets (collected to `/vol/static` in prod)
- `js/` — Existing static JS (served in dev, collected in prod)
- `templates/` — HTML templates
- `vol/static` — (prod) static files for Nginx
- `vol/media` — (prod) media uploads for Nginx
- `nginx/default.conf` — Nginx config for static/media/proxy
- `scripts/entrypoint.prod.sh` — Entrypoint for prod web container

## Environment Variables

- See `.env.dev.example` and `.env.prod.example` for required variables:
	- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`

## Useful Commands

- **Dev server:**
	```sh
	docker compose -f docker-compose.dev.yml --env-file .env.dev up --build
	```
- **Prod server:**
	```sh
	docker compose -f docker-compose.prod.yml --env-file .env.prod up --build
	```
- **Run migrations:**
	```sh
	docker compose -f docker-compose.dev.yml exec web python manage.py migrate
	# or for prod
	docker compose -f docker-compose.prod.yml exec web python manage.py migrate
	```
- **Collect static (prod):**
	```sh
	docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
	```

## Slider CMS: Drag-and-drop Ordering & Preview

- The Slider, SliderItem, and DSPLink models support drag-and-drop ordering in Django admin using django-admin-sortable2.
- To reorder:
  - Use the drag handles in the admin list or inlines for Slider (slot), SliderItem (position), and DSPLink (position).
  - You can also edit the integer fields directly if needed.
- Each Slider change form includes a "Preview" button (top right) that opens a public preview of that slider slot in a new tab.
- You can also preview any slot at `/preview/slider/<slot>/`.

---

**Notes:**
- SQLite is used by default. No DB service is included yet.
- Static files are served from `/static/` in dev, `/vol/static/` in prod (by Nginx).
- Media uploads are served from `/media/` in dev, `/vol/media/` in prod (by Nginx).
