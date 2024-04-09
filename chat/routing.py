from uuid import UUID
from django.urls import re_path

from . import consumers

class UUIDConverter:
    regex = '[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'

    def to_python(self, value):
        return UUID(value)

    def to_url(self, value):
        return str(value)

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_id>%s)/$" % UUIDConverter().regex, consumers.ChatConsumer.as_asgi()),
]