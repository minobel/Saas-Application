import os
from django.test import SimpleTestCase
from django.conf import settings

DATABASE_URL = os.environ.get("DATABASE_URL") or ""


class DatabaseConfigTest(SimpleTestCase):
    def test_database_is_configured(self):
        self.assertIn("default", settings.DATABASES)
        self.assertIn("ENGINE", settings.DATABASES["default"])


class NeonDBTestCase(SimpleTestCase):
    def test_db_url(self):
        db_url = os.environ.get("DATABASE_URL") or ""
        if not db_url or "something.neon.tech" in db_url:
            self.skipTest("Valid DATABASE_URL not found, skipping check.")
        self.assertIn("neon.tech", db_url)
