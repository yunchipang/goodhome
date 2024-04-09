from django.urls import path
from chat.views import get_chat_messages

urlpatterns = [
    path('history/', get_chat_messages, name='chat-history'),
]
