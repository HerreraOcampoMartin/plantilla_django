from .base import *
import os

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [

] # TODO setear bien los dominios permitidos

CORS_ALLOW_ALL_ORIGINS = True
"""CORS_ALLOWED_ORIGINS = [
    "https://frontend.conservatoriofracassi.com.ar",
]"""

# Base de datos
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            # Credenciales (se convierten en AWS_ACCESS_KEY_ID, etc.)
            "access_key": os.environ.get('S3_KEY'),
            "secret_key": os.environ.get('S3_SECRET_KEY'),

            # Endpoint para MinIO
            "endpoint_url": os.environ.get('S3_ENDPOINT_URL'),

            # Nombre del bucket
            "bucket_name": os.environ.get('S3_BUCKET_NAME'),

            # Configuraciones CRÍTICAS para MinIO/S3
            # "url_protocol": os.environ.get('S3_PROTOCOL'),
            "use_ssl": os.environ.get('S3_USE_SSL'),
            # "custom_domain": os.environ.get('S3_CUSTOM_DOMAIN'),
            "querystring_auth": os.environ.get('S3_QUERYSTRING_AUTH'),
            "addressing_style": os.environ.get('S3_ADDRESSING_STYLE')
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
}
