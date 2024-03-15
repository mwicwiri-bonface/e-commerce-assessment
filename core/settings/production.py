from .base import *

CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://www.example.com",
]
HOSTING_PLATFORM = config("HOSTING_PLATFORM")

if HOSTING_PLATFORM == "pythonanywhere":
    # Database
    # https://docs.djangoproject.com/en/5.0/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('POSTGRES_DB_NAME'),
            'USER': config('POSTGRES_DB_USER'),
            'PASSWORD': config('POSTGRES_DB_PASSWORD'),
            'HOST': config('POSTGRES_DB_HOST'),
            'PORT': config('POSTGRES_DB_PORT'),
        }
    }