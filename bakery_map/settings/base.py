import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

from .utils import strtobool

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "{{ secret_key }}",
)

DEBUG = strtobool(os.getenv("DEBUG", "n"))

ALLOWED_HOSTS = [
    s.strip() for s in os.getenv("ALLOWED_HOSTS", "").split(",") if s
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "sass_processor",
    "main",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bakery_map.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "main/templates/",
            BASE_DIR / "templates"
        ],
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

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

WSGI_APPLICATION = "bakery_map.wsgi.application"

# Database

DATABASES = {
    "default": dj_database_url.config(default="sqlite:///db.sqlite3"),
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: E501
    },
]

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
    "pipeline.finders.PipelineFinder",
]

STATICFILES_DIRS = [BASE_DIR / 'main/static']

SASS_PROCESSOR_ROOT = BASE_DIR / "static"
SASS_PROCESSOR_INCLUDE_FILE_PATTERN = r'^.+\.(sass|scss)$'
SASS_PRECISION = 8
SASS_OUTPUT_STYLE = "compressed"
SASS_TEMPLATE_EXTS = [".html", ".haml"]

# User-uploaded files

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)

EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "25"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = EMAIL_PORT == 578
EMAIL_USE_SSL = EMAIL_PORT == 465

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@example.com")

# Logging

SERVER_EMAIL = os.getenv("SERVER_EMAIL", DEFAULT_FROM_EMAIL)

ADMINS = list(
    zip(
        os.getenv("ADMIN_NAMES", "").split(","),
        os.getenv("ADMIN_EMAILS", "").split(","),
    )
)

# django-pipeline (https://django-pipeline.readthedocs.io/en/stable/configuration.html)  # noqa: E501

PIPELINE = {
    "COMPILERS": [
        "pipeline.compilers.sass.SASSCompiler",
    ],
    "SASS_BINARY": "npx sass",
    "SASS_ARGUMENTS": "--style=compressed",
    "CSS_COMPRESSOR": None,  # already compressed by sass compiler
    "JS_COMPRESSOR": "pipeline.compressors.uglifyjs.UglifyJSCompressor",
    "UGLIFYJS_BINARY": "npx terser",
    "UGLIFYJS_ARGUMENTS": "--compress --mangle",
    "STYLESHEETS": {
        # "style": {
        #     "source_filenames": [
        #         "main/css/reset.scss",
        #         "main/css/index.scss"
        #     ],
        #     "output_filename": "main/css/style.css",
        # },
    },
    "JAVASCRIPT": {},
}

# ACCOUNT_AUTHENTICATION_METHOD = "email"
AUTH_USER_MODEL = "main.CustomUser"
ACCOUNT_FORMS = {"signup": "main.forms.SignupForm"}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VARIFICATION = "mandatory"
