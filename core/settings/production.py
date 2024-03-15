from .base import *

CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://www.example.com",
]

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