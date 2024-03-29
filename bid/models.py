from django.db import models


class Property(models.Model):
    category = models.CharField(max_length=50)
    start_bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    seller_id = models.IntegerField()
    created_at = models.DateTimeField()
    property_descr = models.TextField()
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    address = models.CharField(max_length=255)
    squarefeet = models.IntegerField()
    room_type = models.CharField(max_length=50)
    zipcode = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'property'
