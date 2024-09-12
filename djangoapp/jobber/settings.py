import os
from pathlib import Path
import dj_database_url
from decouple import config
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# /data/web/static
# /data/web/media
DATA_DIR = BASE_DIR.parent / "data" / "web"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv("DEBUG", 0)))

# CORS settings
ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()
]

CORS_ALLOWED_ORIGINS = [
    h.strip()
    for h in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if h.strip()
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "jobs",
    "corsheaders",
    "storages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "jobber.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "jobber.wsgi.application"

ON_HEROKU = 'DYNO' in os.environ
print("debug teste",ON_HEROKU)

# DATABASE
if ON_HEROKU:
    # Configurações específicas para o Heroku
    DATABASES = {
        'default': dj_database_url.config(default=config('DATABASE_URL'))
    }
    DEBUG = config('DEBUG', default=False, cast=bool)
else:
    # Configurações específicas para o ambiente local
    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE'),
            'NAME': config('POSTGRES_DB'),
            'USER': config('POSTGRES_USER'),
            'PASSWORD': config('POSTGRES_PASSWORD'),
            'HOST': config('POSTGRES_HOST'),
            'PORT': config('POSTGRES_PORT'),
        }
    }

# AWS
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False


# STATIC FILES
if ON_HEROKU:
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
else:
    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"
    STATIC_ROOT = DATA_DIR / "static"
    MEDIA_ROOT = DATA_DIR / "media"

# Password validation
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
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

REST_FRAMEWORK = {
    "DEFAULT_DATETIME_FORMAT": "d/m/Y",
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
