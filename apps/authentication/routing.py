# routing.py
from django.urls import path, re_path
from .consumer import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/', ChatConsumer.as_asgi()),
    re_path(r"ws/chat2/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
]
