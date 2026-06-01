from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from media_slider.models import Event
from media_slider.seed_events import SEED_EVENTS


class Command(BaseCommand):
    help = "Seed the landing page events from the bundled dummy data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would change without writing to the database.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        created_events = 0
        updated_events = 0

        seed_positions = [event["position"] for event in SEED_EVENTS]
        existing_events = Event.objects.exclude(position__in=seed_positions)
        removed_events = existing_events.count()
        if dry_run:
            self.stdout.write(self.style.WARNING(f"Would delete {removed_events} event(s) not present in seed data."))
        else:
            existing_events.delete()

        for event_data in SEED_EVENTS:
            event_defaults = {
                "title": event_data["title"],
                "event_date": date.fromisoformat(event_data["event_date"]) if event_data.get("event_date") else None,
                "location": event_data.get("location", ""),
                "cta_label": event_data.get("cta_label", "Get Access"),
                "link": event_data.get("link", ""),
                "is_active": True,
            }

            if dry_run:
                event_exists = Event.objects.filter(position=event_data["position"]).exists()
                if event_exists:
                    updated_events += 1
                else:
                    created_events += 1
                continue

            _, was_created = Event.objects.update_or_create(
                position=event_data["position"],
                defaults=event_defaults,
            )
            if was_created:
                created_events += 1
            else:
                updated_events += 1

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run complete. No database changes were made."))
            self.stdout.write(
                f"Would create {created_events} event(s), update {updated_events} event(s)."
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded events: {created_events} created, {updated_events} updated."
            )
        )
