from .base import *

DEBUG = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

# Security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
X_FRAME_OPTIONS = 'DENY'

# Static/Media for Nginx
STATIC_ROOT = BASE_DIR / 'vol/static'
MEDIA_ROOT = BASE_DIR / 'vol/media'

# Whitenoise (optional, fallback if not using nginx)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
