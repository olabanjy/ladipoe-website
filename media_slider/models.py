from django.db import models
from django.core.exceptions import ValidationError

class Slider(models.Model):
    SLOT_CHOICES = [(i, str(i)) for i in range(4)]
    slot = models.PositiveSmallIntegerField(choices=SLOT_CHOICES, unique=True)
    title = models.CharField(max_length=255)
    kind = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    default_video_url = models.URLField(blank=True)
    default_video_file = models.FileField(upload_to="videos/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["slot"]

    def clean(self):
        if not self.default_video_url and not self.default_video_file:
            raise ValidationError("Either default_video_url or default_video_file must be set.")

    def get_video(self):
        if self.default_video_file:
            return self.default_video_file.url
        return self.default_video_url

    def __str__(self):
        return f"Slot {self.slot}: {self.title}"

class SliderItem(models.Model):
    slider = models.ForeignKey(Slider, related_name="items", on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()
    year = models.CharField(max_length=32, blank=True)
    title = models.CharField(max_length=255)
    kind = models.CharField(max_length=255, blank=True)
    meta = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(upload_to="images/", blank=True, null=True)
    youtube_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["position"]
        unique_together = ("slider", "position")

    def clean(self):
        if not self.image_url and not self.image_file:
            raise ValidationError("Either image_url or image_file must be set.")

    def get_image(self):
        if self.image_file:
            return self.image_file.url
        return self.image_url

    def __str__(self):
        return f"{self.title} ({self.year})"

class DSPLink(models.Model):
    item = models.ForeignKey(SliderItem, related_name="dsps", on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=255)
    url = models.URLField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"{self.name} for {self.item}"