from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True


# Base de datos
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'desechable',
        'USER': 'postgres',
        'PASSWORD': 'example',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            # Credenciales (se convierten en AWS_ACCESS_KEY_ID, etc.)
            "access_key": 'minioadmin',
            "secret_key": 'minioadmin',

            # Endpoint para MinIO
            "endpoint_url": 'http://192.168.1.14:9000/',

            # Nombre del bucket
            "bucket_name": 'mi-bucket',

            # Configuraciones CRÍTICAS para MinIO/S3
            # "url_protocol": 'http:', # Usa HTTP para URLs generadas
            "use_ssl": False, # Desactiva SSL para desarrollo local
            # "custom_domain": '192.168.1.14:9000', # Para URLs completas
            "querystring_auth": False, # Para URLs completas
            "addressing_style": 'path', # Para compatibilidad con MinIO
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
}
