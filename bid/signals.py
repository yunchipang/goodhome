from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Auction, Winner, Property, Bid, Bidder, User
from django.utils.timezone import now
from django.contrib.auth import get_user_model


@receiver(post_save, sender=Auction)
def update_winner_on_auction_end(sender, instance, **kwargs):
    if instance.end_time <= now():
        winner = Winner.objects.filter(auction=instance).first()
        if winner and winner.temp_sale_price:
            winner.sale_price = winner.temp_sale_price
            winner.temp_sale_price = None
            winner.save()

            print(f"Updated winner for auction {auction.id}")


@receiver(post_save, sender=Property)
def create_winner_on_property_deactivation(sender, instance, **kwargs):
    print(f"Checking property {instance.id} with is_active={instance.is_active}")
    if not instance.is_active:
        try:
            winner = Winner.objects.get(auction__property=instance)
            print(f"Found winner for auction: {winner}")
            if winner and winner.temp_sale_price:
                winner.sale_price = winner.temp_sale_price
                # winner.temp_sale_price = None
                winner.save()
                print(f"Updated winner: {winner}")
        except Winner.DoesNotExist:
            print("Winner does not exist for this property.")

