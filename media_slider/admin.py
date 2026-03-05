from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import redirect, get_object_or_404
from django.utils.html import format_html

from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin

from .models import Slider, SliderItem, DSPLink


class DSPLinkInline(SortableInlineAdminMixin, admin.TabularInline):
    model = DSPLink
    extra = 0
    fields = ("position", "name", "url", "is_active")
    ordering = ("position",)


class SliderItemInline(SortableInlineAdminMixin, admin.TabularInline):
    model = SliderItem
    extra = 0
    fields = ("position", "year", "title", "kind", "meta", "image_url", "image_file", "youtube_url", "is_active")
    ordering = ("position",)
    show_change_link = True


@admin.register(Slider)
class SliderAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("slot", "title", "kind", "is_active", "preview_link")
    list_display_links = ("slot", "title")
    list_filter = ("is_active",)
    inlines = [SliderItemInline]
    search_fields = ("title", "kind")
    ordering = ("slot",)

    # for the "Preview" button in the change form
    change_form_template = "admin/media_slider/slider/change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "<path:object_id>/preview/",
                self.admin_site.admin_view(self.preview_view),
                name="media_slider_slider_preview",
            ),
        ]
        return custom + urls

    def preview_view(self, request, object_id):
        slider = get_object_or_404(Slider, pk=object_id)
        # Prefer reversing a named URL if you have it; fallback to hardcoded.
        # return redirect(f"/preview/slider/{slider.slot}/")
        return redirect("media_slider:slider_preview", slot=slider.slot)

    @admin.display(description="Preview")
    def preview_link(self, obj):
        if not obj.pk:
            return ""
        url = reverse("admin:media_slider_slider_preview", args=[obj.pk])
        return format_html('<a href="{}" target="_blank" rel="noopener">Preview</a>', url)


@admin.register(SliderItem)
class SliderItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("slider", "position", "title", "year", "is_active")
    list_filter = ("slider", "is_active")
    inlines = [DSPLinkInline]
    search_fields = ("title", "year", "kind", "meta")
    # Prefer sorting by position for sortable list UX
    ordering = ("position",)


@admin.register(DSPLink)
class DSPLinkAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("item", "position", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "url")
    ordering = ("position",)
