from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Property(models.Model):
    category = models.CharField(max_length=50)
    start_bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    property_descr = models.TextField()
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    address = models.CharField(max_length=255)
    squarefeet = models.IntegerField(null=True, blank=True)
    room_type = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "property"


class Auction(models.Model):
    property = models.ForeignKey(Property, related_name='auctions', on_delete=models.CASCADE)
    current_highest_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Auction for {self.property.title}"
