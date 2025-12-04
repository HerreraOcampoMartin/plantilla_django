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
