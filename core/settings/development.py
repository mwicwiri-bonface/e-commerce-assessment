from .base import *

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE.insert(2, "debug_toolbar.middleware.DebugToolbarMiddleware")
