import os
from pathlib import Path
import dj_database_url
from decouple import config
import psycopg

from decouple import config

STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default="")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------
# Secret & Debug
# ----------------------
BASE_URL = config('BASE_URL', default=None)
SECRET_KEY = config('DJANGO_SECRET_KEY')
DEBUG = config('DJANGO_DEBUG', cast=bool, default=True)
ALLOWED_HOSTS = [".railway.app"]
if DEBUG:
    ALLOWED_HOSTS += ["127.0.0.1", "localhost"]

# ----------------------
# Email Configuration
# ----------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config("EMAIL_HOST", cast=str, default=None)
EMAIL_PORT = config("EMAIL_PORT", cast=int, default=587)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str, default=None)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str, default=None)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=False)

# ----------------------
# Admins
# ----------------------
ADMIN_USER_NAME = config('ADMIN_USER_NAME', default='Admin user')
ADMIN_USER_EMAIL = config('ADMIN_USER_EMAIL', default=None)

MANAGERS = []
ADMINS = []
if all([ADMIN_USER_NAME, ADMIN_USER_EMAIL]):
    ADMINS.append((ADMIN_USER_NAME, ADMIN_USER_EMAIL))
    MANAGERS = ADMINS

# ----------------------
# Installed Apps
# ----------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third Party Apps
    'allauth_ui',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'slippers',
    'widget_tweaks',

    # Your Apps
    'commando',
    'visits',
    'profiles',
    'subscriptions',
    'customers',
    'checkouts',
]

# ----------------------
# Middleware
# ----------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cfehome.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cfehome.wsgi.application'

# ----------------------
# Database (Postgres or SQLite fallback)
# ----------------------
DATABASE_URL = config('DATABASE_URL', default=None)

def get_database_config():
    if DATABASE_URL:
        try:
            # Test connection to PostgreSQL
            conn = psycopg.connect(DATABASE_URL)
            conn.close()
            return dj_database_url.config(default=DATABASE_URL, conn_max_age=30, conn_health_checks=True)
        except Exception:
            print("WARNING: PostgreSQL not reachable, falling back to SQLite")
    # Fallback SQLite
    return {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

DATABASES = {
    'default': get_database_config()
}

# ----------------------
# Password validation
# ----------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ----------------------
# Django Allauth
# ----------------------
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[CFE Home] "
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "VERIFIED_EMAIL": False,
        "SCOPE": [
            "user:email",
            "read:user",
        ],
    }
}

# ----------------------
# Internationalization
# ----------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------
# Static files
# ----------------------
STATIC_URL = 'static/'
STATICFILES_BASE_DIR = BASE_DIR / 'staticfiles'
STATICFILES_BASE_DIR.mkdir(parents=True, exist_ok=True)
STATICFILES_VENDOR_DIR = STATICFILES_BASE_DIR / "vendors"
STATICFILES_DIRS = [STATICFILES_BASE_DIR]

STATIC_ROOT = BASE_DIR / 'local_cdn'
if not DEBUG:
    STATIC_ROOT = BASE_DIR / 'prod-cdn'

STORAGES = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}

WHITENOISE_MANIFEST_STRICT = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'
SITE_ID = 2



