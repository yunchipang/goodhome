from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    pass  # 空的管理类，以便注册自定义的用户模型


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

