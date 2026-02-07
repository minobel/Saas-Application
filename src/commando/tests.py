import os
from django.test import TestCase
from django.conf import settings

DATABASE_URL = os.environ.get("DATABASE_URL") or ""


class DatabaseConfigTest(TestCase):
    def test_database_is_configured(self):
        self.assertIn("default", settings.DATABASES)
        self.assertIn("ENGINE", settings.DATABASES["default"])


class NeonDBTestCase(TestCase):
    def test_db_url(self):
        self.assertIn("neon.tech", DATABASE_URL)
