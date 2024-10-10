"""
ASGI config for vouchers_system project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vouchers_system.settings")

import django
django.setup()

from django.core.management import call_command

# import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import member.routing 

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vouchers_system.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles traditional HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            member.routing.websocket_urlpatterns  # We'll define WebSocket routes in the member app
        )
    ),
})