from django.urls import path
from social_media.consumers import FeedConsumer

websocket_urlpatterns = [
    path('ws/feed/', FeedConsumer.as_asgi()),
]
