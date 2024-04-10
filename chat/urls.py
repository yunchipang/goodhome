from django.urls import path
from chat.views import get_chat_messages, get_last_chat

urlpatterns = [
    path('history/', get_chat_messages, name='chat-history'),
    path('last/', get_last_chat, name='last-chat')
]
