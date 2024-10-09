from django.urls import path
from .consumers import VoucherConsumer

websocket_urlpatterns = [
    path('ws/voucher/', VoucherConsumer.as_asgi()),
]
