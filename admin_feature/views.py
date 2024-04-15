from django.http import JsonResponse
from bid.models import User

print(User.objects.count())

def stats_view(request):
    # 你可以在这里实现一些逻辑来获取数据
    total_users = User.objects.count()  # 计算总用户数
    # 你可以在这里添加更多的统计数据，如在线用户数、今日活跃用户等

    return JsonResponse({
        'total_users': total_users,
        # 添加其他统计数据
    })