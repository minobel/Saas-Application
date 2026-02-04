from django.test import TestCase
from django.conf import settings

class DatabaseConfigTest(TestCase):
    def test_database_is_configured(self):
        self.assertIn("default", settings.DATABASES)
        self.assertIn("ENGINE", settings.DATABASES["default"])

