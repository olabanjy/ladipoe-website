import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

django_app = get_asgi_application()

from django.conf import settings
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

# ✅ Use Django's DEBUG, not a separate env var
application = ASGIStaticFilesHandler(django_app) if settings.DEBUG else django_app
