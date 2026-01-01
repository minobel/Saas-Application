import os
from pathlib import Path
import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings
SECRET_KEY = config('DJANGO_SECRET_KEY')
DEBUG = config('DJANGO_DEBUG', cast=bool)

ALLOWED_HOSTS = [".railway.app"]
if DEBUG:
    ALLOWED_HOSTS += ["127.0.0.1", "localhost"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'commando',
    'visits',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ADDED: WhiteNoise middleware to serve static files on Railway
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
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

# Database settings
DATABASE_URL = config('DATABASE_URL', default=None)
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=30,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- STATIC FILES CONFIGURATION ---
STATIC_URL = 'static/'

# CHANGED: Ensure this points to the correct folder where your local CSS/JS are
STATICFILES_BASE_DIR = BASE_DIR / 'staticfiles'

# FIXED: Ensure the directory exists to avoid the (staticfiles.W004) warning

STATICFILES_BASE_DIR.mkdir(parents=True, exist_ok=True)
STATICFILES_DIRS = [
    STATICFILES_BASE_DIR
]

# FIXED: Standardized names for local and production CDNs
STATIC_ROOT = BASE_DIR / 'local_cdn'
if not DEBUG:
    STATIC_ROOT = BASE_DIR / 'prod-cdn'

# ADDED: Storage engine for WhiteNoise (Optimizes CSS/JS compression)
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Added STATICFILES_VENDOR_DIR for vendor files
STATICFILES_VENDOR_DIR = BASE_DIR / 'staticfiles/vendors'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

