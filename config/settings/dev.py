from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", ".local"]
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]


INSTALLED_APPS += [
    # Add dev-only apps here
     "django_browser_reload",
]
MIDDLEWARE += [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
] 
# Use default STATICFILES_DIRS for dev (js/, static/)
ASGI_APPLICATION = "config.asgi.application"
