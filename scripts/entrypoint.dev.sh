#!/bin/sh
set -e

echo "Waiting for DB..."
sh /app/scripts/wait_for_db.sh
echo "DB is ready"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static..."
python manage.py collectstatic --noinput || {
  echo "⚠️ collectstatic failed (dev can still run without it)."
}
echo "Static collected."

echo "Ensuring admin superuser exists..."

python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
from django.conf import settings
import secrets

User = get_user_model()

username = 'admin'

if not User.objects.filter(username=username).exists():
    password = secrets.token_urlsafe(16)

    User.objects.create_superuser(
        username=username,
        email='admin@example.com',
        password=password
    )

    env_path = os.path.join(settings.BASE_DIR, '.env.dev')

    with open(env_path, 'a') as f:
        f.write(f'\nDJANGO_ADMIN_PASSWORD={password}\n')

    print('✅ Admin user created')
    print(f'   username: admin')
    print(f'   password: {password}')
else:
    print('ℹ️ Admin user already exists')
"

echo "Starting dev server..."
exec "$@"
