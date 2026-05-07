from django.core.management.base import BaseCommand
from django.db import transaction

from media_slider.models import DSPLink, Slider, SliderItem
from media_slider.seed_data import SEED_SLIDERS


class Command(BaseCommand):
    help = "Seed slider content from the bundled Ladipoe homepage data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would change without writing to the database.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        created_sliders = 0
        updated_sliders = 0
        created_items = 0
        updated_items = 0
        created_dsps = 0
        updated_dsps = 0

        seed_slots = [slider["slot"] for slider in SEED_SLIDERS]
        existing_sliders = Slider.objects.exclude(slot__in=seed_slots)
        removed_sliders = existing_sliders.count()
        if dry_run:
            self.stdout.write(self.style.WARNING(f"Would delete {removed_sliders} slider(s) not present in seed data."))
        else:
            existing_sliders.delete()

        for slider_data in SEED_SLIDERS:
            slider_defaults = {
                "title": slider_data["title"],
                "kind": slider_data["kind"],
                "is_active": True,
                "default_video_url": slider_data["default_video_url"],
            }

            if dry_run:
                slider = Slider.objects.filter(slot=slider_data["slot"]).first()
                if slider:
                    updated_sliders += 1
                else:
                    created_sliders += 1
            else:
                slider, was_created = Slider.objects.update_or_create(
                    slot=slider_data["slot"],
                    defaults=slider_defaults,
                )
                if was_created:
                    created_sliders += 1
                else:
                    updated_sliders += 1

            if dry_run:
                seed_positions = [item["position"] for item in slider_data["items"]]
                existing_items = slider.items.exclude(position__in=seed_positions) if slider else []
                removed_items = existing_items.count() if slider else 0
                if removed_items:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Would delete {removed_items} item(s) from slot {slider_data['slot']} not present in seed data."
                        )
                    )
            else:
                seed_positions = [item["position"] for item in slider_data["items"]]
                existing_items = slider.items.exclude(position__in=seed_positions)
                existing_items.delete()

            for item_data in slider_data["items"]:
                item_defaults = {
                    "year": item_data["year"],
                    "title": item_data["title"],
                    "kind": item_data["kind"],
                    "meta": item_data["meta"],
                    "image_url": item_data["image_url"],
                    "youtube_url": item_data["youtube_url"],
                    "is_active": True,
                }

                if dry_run:
                    item = slider.items.filter(position=item_data["position"]).first() if slider else None
                    if item:
                        updated_items += 1
                    else:
                        created_items += 1
                else:
                    item, was_created = SliderItem.objects.update_or_create(
                        slider=slider,
                        position=item_data["position"],
                        defaults=item_defaults,
                    )
                    if was_created:
                        created_items += 1
                    else:
                        updated_items += 1

                if dry_run:
                    if not item:
                        created_dsps += len(item_data["dsps"])
                    else:
                        seed_dsp_positions = [dsp["position"] for dsp in item_data["dsps"]]
                        existing_dsps = item.dsps.exclude(position__in=seed_dsp_positions)
                        removed_dsps = existing_dsps.count()
                        if removed_dsps:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Would delete {removed_dsps} DSP link(s) for {item.title} not present in seed data."
                                )
                            )
                else:
                    seed_dsp_positions = [dsp["position"] for dsp in item_data["dsps"]]
                    existing_dsps = item.dsps.exclude(position__in=seed_dsp_positions)
                    existing_dsps.delete()

                for dsp_data in item_data["dsps"]:
                    dsp_defaults = {
                        "name": dsp_data["name"],
                        "url": dsp_data["url"],
                        "is_active": True,
                    }

                    if dry_run:
                        if item:
                            dsp_exists = item.dsps.filter(position=dsp_data["position"]).exists()
                            if dsp_exists:
                                updated_dsps += 1
                            else:
                                created_dsps += 1
                        else:
                            created_dsps += 1
                    else:
                        _, was_created = DSPLink.objects.update_or_create(
                            item=item,
                            position=dsp_data["position"],
                            defaults=dsp_defaults,
                        )
                        if was_created:
                            created_dsps += 1
                        else:
                            updated_dsps += 1

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run complete. No database changes were made."))
            self.stdout.write(
                f"Would create {created_sliders} slider(s), update {updated_sliders} slider(s), "
                f"create {created_items} item(s), update {updated_items} item(s), "
                f"create {created_dsps} DSP link(s), update {updated_dsps} DSP link(s)."
            )
            return

        self.stdout.write(self.style.SUCCESS(
            f"Seeded slider content: {created_sliders} created, {updated_sliders} updated; "
            f"{created_items} items created, {updated_items} updated; "
            f"{created_dsps} DSP links created, {updated_dsps} updated."
        ))
