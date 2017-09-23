import os
from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8p8van&gi*o!q+&7w*adc@+j^gy#wyeu&u1klk%d+yuq&#4)4b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
