from django.apps import AppConfig
from django.db.models.signals import post_save


class BidConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bid"

    def ready(self):
        # 导入信号处理函数
        from .signals import create_winner_on_property_deactivation
        # 连接信号
        post_save.connect(create_winner_on_property_deactivation, sender='bid.Property')
