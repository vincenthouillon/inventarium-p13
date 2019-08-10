"""Django travis settings for inventarium project."""

from . import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'inventarium',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}
