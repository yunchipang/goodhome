from django.conf import settings
from core import settings
from django.db import models
from django.utils import timezone

# Create your models here.
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

# Custom User Model


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

# Seller Model


class Seller(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"Seller: {self.user.username}"

    class Meta:
        db_table = "seller"

# Bidder Model


class Bidder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        # return f"Bidder: {self.user.username}"
        return self.user.username

    class Meta:
        db_table = "bidder"


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
    image_url = models.ImageField(upload_to='image_url/')


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'property'


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


class Bid(models.Model):
    bidder = models.ForeignKey(
        Bidder, on_delete=models.CASCADE, db_column='bidder_id')
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name='bids', db_column='auction_id')
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.amount} by {self.bidder}"

    class Meta:
        db_table = "bid"


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


class WinnerRating(models.Model):
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ratings_given',
        db_column='seller_id',  # 指定数据库中的列名
    )
    winner = models.ForeignKey(
        User,  # 直接关联到User模型
        on_delete=models.CASCADE,
        related_name='ratings_received',
        db_column='winner_id',  # 指定数据库中的列名
    )
    message = models.CharField(max_length=100)
    rating = models.IntegerField(
        choices=[(1, 'Poor'), (2, 'Average'), (3, 'Good'),
                 (4, 'Very Good'), (5, 'Excellent')]
    )

    def __str__(self):
        # 由于现在winner直接关联到User，因此直接使用winner.username
        return f"Rating from {self.seller.username} to {self.winner.username}: {self.rating} - {self.message}"

    class Meta:
        db_table = "winner_rating"


class ShippingGift(models.Model):
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shipments_made',
        db_column='seller_id',  # Specifies the column name in the database
    )
    winner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shipments_received',
        db_column='winner_id',  # Specifies the column name in the database
    )
    ups_tracking_number = models.CharField(max_length=50)

    def __str__(self):
        # Here we use seller.username and winner.username assuming they are linked to the User model
        return f"Shipment from {self.seller.username} to {self.winner.username} with tracking number {self.ups_tracking_number}"

    class Meta:
        db_table = "shipping"
