from django.http import JsonResponse
from .models import ChatMessage
from django.db.models import Q


def get_chat_messages(request):
    user1_id = request.GET.get('user1_id')
    user2_id = request.GET.get('user2_id')
    
    messages = ChatMessage.objects.filter(
        (Q(sender_id=user1_id) & Q(receiver_id=user2_id)) |
        (Q(sender_id=user2_id) & Q(receiver_id=user1_id))
    ).order_by('timestamp').values('sender_id', 'receiver_id', 'message', 'timestamp')
    
    return JsonResponse(list(messages), safe=False)
