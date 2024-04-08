# from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# from django.db import models



# # Create your models here.
# from django.contrib.auth.models import User

# from core import settings
# from django.conf import settings

# # Custom User Manager
# class UserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('Users must have an email address')
#         if not username:
#             raise ValueError('Users must have a username')

#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#             **extra_fields
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(username, email, password, **extra_fields)


# # Custom User Model
# class User(AbstractBaseUser):
#     last_login = models.DateTimeField(blank=True, null=True)
#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(max_length=100, unique=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     password = models.CharField(max_length=255)
#     phone = models.CharField(max_length=50, blank=True, null=True)
#     mailing_address = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     objects = UserManager()

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     def __str__(self):
#         return self.username

#     class Meta:
#         db_table = "user"
#         app_label = 'authentication'
