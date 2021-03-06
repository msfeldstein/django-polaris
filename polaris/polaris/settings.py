"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
# pylint: disable=invalid-name
import os
from shutil import copyfile

import environ
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from stellar_sdk.server import Server
from stellar_sdk.keypair import Keypair


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env
env = environ.Env()

# Use the directory of the django project that installed this app
# Or if undefined, use outer directory for this app
try:
    PROJECT_ROOT = settings.PROJECT_ROOT
except ImproperlyConfigured:
    PROJECT_ROOT = os.path.dirname(BASE_DIR)
    copyfile(os.path.join(PROJECT_ROOT, ".env.example"), os.path.join(PROJECT_ROOT, ".env"))

env_file = os.path.join(PROJECT_ROOT, ".env")
if os.path.exists(env_file):
    environ.Env.read_env(str(env_file))

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", False)

STELLAR_DISTRIBUTION_ACCOUNT_SEED = env("STELLAR_DISTRIBUTION_ACCOUNT_SEED")
STELLAR_DISTRIBUTION_ACCOUNT_ADDRESS = (
    Keypair.from_secret(STELLAR_DISTRIBUTION_ACCOUNT_SEED).public_key
)
STELLAR_ISSUER_ACCOUNT_ADDRESS = env("STELLAR_ISSUER_ACCOUNT_ADDRESS")
STELLAR_NETWORK_PASSPHRASE = env("STELLAR_NETWORK_PASSPHRASE", default="Test SDF Network ; September 2015")
HORIZON_URI = env("HORIZON_URI", default="https://horizon-testnet.stellar.org/")
HORIZON_SERVER = Server(horizon_url=HORIZON_URI)
SERVER_JWT_KEY = env("SERVER_JWT_KEY")
OPERATION_DEPOSIT = "deposit"
OPERATION_WITHDRAWAL = "withdraw"
ACCOUNT_STARTING_BALANCE = str(2.01)

# Apps to add to parent project's INSTALLED_APPS
django_apps = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
third_party_apps = ["rest_framework", "corsheaders"]
INSTALLED_APPS = django_apps + third_party_apps + ["polaris"]

# Modules to add to parent project's MIDDLEWARE
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

APPEND_SLASH = False

ROOT_URLCONF = "polaris.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": env.db(
        "DATABASE_URL", default="sqlite:///" + os.path.join(PROJECT_ROOT, "db.sqlite3")
    )
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "polaris/static")
STATIC_URL = "/polaris/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'polaris/static'),
)

# Django Rest Framework Settings:
# Attributes to add to parent project's REST_FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_RENDERER_CLASSES": [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer'
    ],
    "PAGE_SIZE": 10,
}

# API Config

DEFAULT_PAGE_SIZE = 10

# CORS configuration

CORS_ORIGIN_ALLOW_ALL = True
