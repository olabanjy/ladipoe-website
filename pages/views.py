# pages/views.py (or wherever home currently lives)
from django.shortcuts import render
from media_slider.models import Slider
import json


def _build_playlist():
    sliders = (
        Slider.objects.filter(is_active=True)
        .prefetch_related("items__dsps")
        .order_by("slot")
    )

    playlist = []
    for slider in sliders:
        video = slider.get_video()
        nav = []
        for item in slider.items.filter(is_active=True).order_by("position"):
            img = item.get_image()
            dsps = [
                {"name": d.name, "url": d.url}
                for d in item.dsps.filter(is_active=True).order_by("position")
            ]
            nav.append({
                "year": item.year,
                "title": item.title,
                "kind": item.kind,
                "meta": item.meta,
                "img": img,
                "dsps": dsps,
                "youtube": item.youtube_url,
            })

        playlist.append({"slot": slider.slot, "video": video, "nav": nav})

    return sliders, json.dumps(playlist)


def home(request):
    sliders, playlist_json = _build_playlist()
    return render(request, "index.html", {
        "playlist_json": playlist_json,
        "sliders": sliders,
        "preview_slot": None,
    })


def slider_preview(request, slot: int):
    sliders, playlist_json = _build_playlist()
    slot = int(slot)
    available_slots = {s.slot for s in sliders}
    if slot not in available_slots:
        slot = None
    return render(request, "index.html", {
        "playlist_json": playlist_json,
        "sliders": sliders,
        "preview_slot": slot,
    })
