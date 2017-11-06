from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'smart_water',
        'USER': 'smart_water',
        'PASSWORD': 'smart_water12345678',
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
    }
}

STATIC_ROOT = os.path.join(PROJECT_DIR,'static')

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
