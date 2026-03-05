
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "POE Admin"
admin.site.site_title = "POE Admin"
admin.site.index_title = "Platform Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path("", include("media_slider.urls")),  # preview route lives here
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
