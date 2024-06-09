# -*- coding: utf-8 -*-
"""
Django settings for sweepstake project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import pytz
from pathlib import Path
from urllib.parse import urlparse

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-t4@++_fy&@8e670&&s)6p+2glp-o&ms2&_&hc6b!z64q(4pueq"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MAIN_HOST = os.environ.get("MAIN_HOST", "http://localhost")
HOSTS = os.environ.get("HOSTS", "http://localhost,http://127.0.0.1/,http://0.0.0.0/").split(",")
CSRF_TRUSTED_ORIGINS = HOSTS
ALLOWED_HOSTS = [urlparse(url).netloc for url in HOSTS]
CORS_ALLOWED_ORIGINS = HOSTS


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "general",
    "competition",
]
AUTH_USER_MODEL = "general.CustomUser"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "sweepstake.urls"

MIGRATION_MODULES = {
    "general": "data.db_migrations.general",
    "competition": "data.db_migrations.competition",
    "preferences": "data.db_migrations.preferences",
    # "django_celery_beat": "data.db_migrations.django_celery_beat",
    "sessions": "data.db_migrations.sessions",
    "auth": "data.db_migrations.auth",
    "authtoken": "data.db_migrations.authtoken",
    "admin": "data.db_migrations.admin",
    "contenttypes": "data.db_migrations.contenttypes",
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sweepstake.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "data/db.sqlite3",
        "OPTIONS": {
            "timeout": 20,  # seconds
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = CELERY_TIMEZONE = os.getenv("TIME_ZONE", "Europe/London")
TIME_ZONE_OBJ = pytz.timezone(TIME_ZONE)

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

WHITENOISE_STATIC_PREFIX = "/static/"
STATIC_ROOT = BASE_DIR / "productionfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
