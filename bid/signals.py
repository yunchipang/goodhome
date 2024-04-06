from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Auction, Winner
from django.utils.timezone import now

@receiver(post_save, sender=Auction)
def update_winner_on_auction_end(sender, instance, **kwargs):
    if instance.end_time <= now():
        winner = Winner.objects.filter(auction=instance).first()
        if winner and winner.temp_sale_price:
            winner.sale_price = winner.temp_sale_price
            winner.temp_sale_price = None
            winner.save()

            print(f"Updated winner for auction {auction.id}")


