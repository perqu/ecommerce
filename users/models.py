import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

gender_choices = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class Address(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.street} {self.house_number}, {self.postal_code} {self.city}"

class UserProfile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    # profile
    gender = models.CharField(max_length=1, choices=gender_choices, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    # address
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True, to_field='uuid')
    phone_number = models.CharField(max_length=15, blank=True)

    class Meta:
        verbose_name = "User profile"
        verbose_name_plural = "User profiles"
    
class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    password = models.CharField(max_length=128, blank=False)
    email_verified = models.BooleanField(default=False)
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='user_profile', null=True, blank=True, to_field='uuid')

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
    



