# Generated manually to add admin-managed landing page events.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("media_slider", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("position", models.PositiveSmallIntegerField(default=0)),
                ("title", models.CharField(max_length=255)),
                ("event_date", models.DateField(blank=True, null=True)),
                ("location", models.CharField(blank=True, max_length=255)),
                ("cta_label", models.CharField(default="Get Access", max_length=255)),
                ("link", models.URLField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["position", "event_date", "title"],
            },
        ),
    ]
