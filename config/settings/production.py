import os
from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8p8van&gi*o!q+&7w*adc@+j^gy#wyeu&u1klk%d+yuq&#4)4b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
