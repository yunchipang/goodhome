from django.apps import AppConfig


class BidConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bid"

class AuctionsConfig(AppConfig):
    name = 'bid'

    def ready(self):
        # 导入信号接收器，确保它在 Django 启动时被注册
        from . import signals
