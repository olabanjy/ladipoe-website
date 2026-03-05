#!/bin/sh
# entrypoint for prod: run migrations, collectstatic, then exec gunicorn
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
