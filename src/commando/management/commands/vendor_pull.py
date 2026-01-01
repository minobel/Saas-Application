import helpers
from typing import Any
from django.conf import settings
from django.core.management.base import BaseCommand


STATICFILES_VENDOR_DIR = getattr(settings, 'STATICFILES_VENDOR_DIR')
VENDOR_STATICFILES = {
    "flowbite.min.css": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css",
    "flowbite.min.js": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js",
}

class Command(BaseCommand):

    def handle(self, *args: any, **options: any):
        self.stdout.write("Downloading vendor static files...")
        completed_urls = []
        for name, url in VENDOR_STATICFILES.items():
            out_path = STATICFILES_VENDOR_DIR / name
            dl_success = helpers.download_to_local(url, out_path)
            if dl_success:
                completed_urls.append(url)
                self.stdout.write(f"Downloaded: {url} to {out_path}")
            else:
                self.stderr.write(
                    self.style.ERROR(f"Failed to download: {url}")
                )
            if set(completed_urls) == set(VENDOR_STATICFILES.values()):
                self.stdout.write(
                    self.style.SUCCESS("All vendor static files downloaded successfully.")
                )
            else:
                self.stdout.write(
                    self.style.WARNING("Some vendor static files failed to download.")
                )