from django.db import models
from django.utils import timezone


class Property(models.Model):
    category = models.CharField(max_length=50)
    start_bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    seller_id = models.IntegerField()
    # created_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    property_descr = models.TextField()
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    address = models.CharField(max_length=255)
    squarefeet = models.IntegerField()
    room_type = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    image_url = models.ImageField(upload_to='image_url/')

    class Meta:
        db_table = 'property'


class User(AbstractBaseUser):
    last_login = models.DateTimeField(blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True, null=True)
    mailing_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user"


class Auction(models.Model):
    property = models.ForeignKey(
        Property, related_name='auctions', on_delete=models.CASCADE)
    current_highest_bid = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Auction for {self.property.title}"

    class Meta:
        db_table = "auction"


class Winner(models.Model):
    auction = models.OneToOneField(
        Auction, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    temp_sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        winner = self.user.username if self.user else "No winner yet"
        return f"Winner of Auction {self.auction.id}: {winner}"

    class Meta:
        db_table = "winner"
