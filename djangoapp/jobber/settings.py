"""
Django settings for jobber project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# /data/web/static
# /data/we/media
DATA_DIR = BASE_DIR.parent / "data" / "web"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv("DEBUG", 0)))


ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()
]

# Configurações CORS
CORS_ALLOWED_ORIGINS = [
    h.strip()
    for h in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")  # noqa
    if h.strip()
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

# Configurações AWS S3
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='sa-east-1')

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

AWS_DEFAULT_ACL = None  # Garantir que os arquivos tenham controle de acesso correto
AWS_QUERYSTRING_AUTH = False  # Evita que o URL gerado contenha tokens de autenticação
AWS_S3_VERITY = True  # Verificar se a configuração de verificação de SSL está ativa
AWS_S3_FILE_OVERWRITE = False

STORAGES = {

    # Media file (image) management
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage"
    },

    # Staticfiles management
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage"
    },
}

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Verifique se estamos no Heroku
ON_HEROKU = 'DYNO' in os.environ

if ON_HEROKU:
    # Configurações específicas para o Heroku
    DATABASES = {
        'default': dj_database_url.config(default=config('DATABASE_URL'))
    }
    DEBUG = config('DEBUG', default=False, cast=bool)

    # Usando o AWS S3
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
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


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
# /data/web/static
STATIC_ROOT = DATA_DIR / "static"

MEDIA_URL = "/media/"
# /data/web/media
MEDIA_ROOT = DATA_DIR / "media"

REST_FRAMEWORK = {
    "DEFAULT_DATETIME_FORMAT": "d/m/Y",
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field


# # Configuração para upload de arquivos
# FILE_UPLOAD_STORAGE = config("FILE_UPLOAD_STORAGE", default="local")

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# # Configurações de arquivos estáticos e mídia local
# STATIC_URL = "/static/"
# STATIC_ROOT = DATA_DIR / "static"

# MEDIA_URL = "/media/"
# MEDIA_ROOT = DATA_DIR / "media"

# # Configurações de produção (AWS S3)
# if FILE_UPLOAD_STORAGE == "s3":
#     # Armazenamento S3 para arquivos de mídia
#     DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

#     # Armazenamento S3 para arquivos estáticos
#     STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

#     # Nome do bucket no S3
#     AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")

#     # Configurações AWS (credenciais)
#     AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
#     AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
#     AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", default="sa-east-1")

#     # URL de acesso aos arquivos estáticos e de mídia no S3
#     AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

#     # Configurar URLs para servir arquivos estáticos e mídia
#     STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
#     MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"


#     # Outras configurações do S3
#     AWS_DEFAULT_ACL = None  # Melhor para evitar problemas de permissões
#     AWS_S3_FILE_OVERWRITE = False  # Evitar sobrescrever arquivos com o mesmo nome
#     AWS_QUERYSTRING_AUTH = False   # Remove parâmetros de autenticação das URLs geradas

# Configuração para upload de arquivos
# FILE_UPLOAD_STORAGE = config("FILE_UPLOAD_STORAGE", default="local")

# if ON_HEROKU or FILE_UPLOAD_STORAGE == "s3":
#     # Configuração de armazenamento S3
#     DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
#     STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

#     # Nome do bucket no S3
#     AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
#     AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
#     AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
#     AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", default="sa-east-1")

#     AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
#     STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
#     MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

#     AWS_DEFAULT_ACL = None
#     AWS_S3_FILE_OVERWRITE = False
#     AWS_QUERYSTRING_AUTH = False
# else: 
#     STATIC_URL = "/static/"
#     STATIC_ROOT = DATA_DIR / "static"
#     MEDIA_URL = "/media/"
#     MEDIA_ROOT = DATA_DIR / "media"
