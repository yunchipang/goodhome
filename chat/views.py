from django.http import JsonResponse
from chat.models import ChatMessage
from bid.models import User
from django.db.models import Q


def get_chat_messages(request):
    user1_id = request.GET.get('user1_id')
    user2_id = request.GET.get('user2_id')
    
    messages = ChatMessage.objects.filter(
        (Q(sender_id=user1_id) & Q(receiver_id=user2_id)) |
        (Q(sender_id=user2_id) & Q(receiver_id=user1_id))
    ).order_by('timestamp').values('sender_id', 'receiver_id', 'message', 'timestamp')
    
    return JsonResponse(list(messages), safe=False)

def get_last_chat(request):
    user_id = request.GET.get('user_id')
    
    # Retrieve the last message for each conversation the current user has participated in
    last_messages = {}
    conversations = ChatMessage.objects.filter(
        Q(sender_id=user_id) | Q(receiver_id=user_id)
    ).order_by('-timestamp')  # Order by timestamp descending to get the latest message first

    for conversation in conversations:
        other_party_id = conversation.sender_id if conversation.receiver_id == int(user_id) else conversation.receiver_id
        if other_party_id not in last_messages:
            last_messages[other_party_id] = conversation.message
    
    # Retrieve user details and last message for each conversation
    users_info = []
    for other_party_id, last_message in last_messages.items():
        other_party_info = User.objects.filter(id=other_party_id).values('id', 'username').first()
        if other_party_info:
            other_party_info['last_message'] = last_message
            users_info.append(other_party_info)
    
    return JsonResponse(users_info, safe=False)
