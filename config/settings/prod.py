from .base import *

DEBUG = False
ALLOWED_HOSTS = env('ALLOWED_HOSTS', default=[])

# Security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static/Media for Nginx
STATIC_ROOT = BASE_DIR / 'vol/static'
MEDIA_ROOT = BASE_DIR / 'vol/media'

# Whitenoise (optional, fallback if not using nginx)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
