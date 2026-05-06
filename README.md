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

	 - Gunicorn runs Django app on port `127.0.0.1:8001` by default.
	 - Static and media files are bind-mounted so the host Nginx can serve them directly.
	 - Entrypoint script runs migrations and collectstatic automatically.

3. Put a host-level Nginx in front of the compose stack for TLS termination and public traffic.

4. To run management commands in the web container:

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
- `nginx/default.conf` — optional Nginx config template
- `scripts/entrypoint.prod.sh` — Entrypoint for prod web container

## Environment Variables

- See `.env.dev.example` and `.env.prod.example` for required variables:
	- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`

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

## Remote Server Nginx + SSL

Use the host Nginx to terminate TLS, serve static/media from the bind-mounted directories, and forward app traffic to the compose stack at `127.0.0.1:8001`.

1. Point your domain DNS `A` record to the server IP.
2. Open firewall ports `80` and `443`.
3. Install Nginx and Certbot on the host.
4. Start the compose stack so the app is reachable on `127.0.0.1:8001`.
5. Configure host Nginx to serve static/media from the repo's `vol/static` and `vol/media` directories.
6. Configure host Nginx to proxy app requests to `http://127.0.0.1:8001`.
7. Issue a Let's Encrypt certificate with Certbot and reload Nginx.

Example host Nginx config:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location /static/ {
        alias /srv/poe/vol/static/;
        access_log off;
        expires 30d;
    }

    location /media/ {
        alias /srv/poe/vol/media/;
        access_log off;
        expires 30d;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-Host $host;
    }
}
```

Certbot example:

```sh
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

After installation, verify that:

- the app responds at `https://yourdomain.com`
- static files load correctly
- `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` match your domain names

---

**Notes:**
- SQLite is used by default in local development.
- Static files are served from `/static/` in dev and `/vol/static/` in prod.
- Media uploads are served from `/media/` in dev and `/vol/media/` in prod.
- Production uses Postgres in Docker and expects the host Nginx to proxy TLS traffic to `127.0.0.1:8001`.
