"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from config.routing import websocket_urlpatterns
from social_media.middlewares import JWTTokenAuthMiddleware


configuration = os.getenv('ENVIRONMENT', 'development').title()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', configuration)

from configurations import importer  # noqa
importer.install()

from django.core.asgi import get_asgi_application   # noqa
# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTTokenAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})