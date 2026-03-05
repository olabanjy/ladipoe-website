# media_slider/urls.py
from django.urls import path
from pages import views  # reuse existing view, or move preview view into media_slider/views.py

app_name = "media_slider"

urlpatterns = [
    path("preview/slider/<int:slot>/", views.slider_preview, name="slider_preview"),
]
