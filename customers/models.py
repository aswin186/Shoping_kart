from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class UserProfile(models.Model):
    live = 1
    delete = 0
    user_status = ((live, 'Live'), (delete, 'Delete'))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    name = models.CharField(max_length=120, null=True)
    # address = models.CharField(max_length=120)
    phone = models.CharField(max_length=120, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delete_status = models.IntegerField(choices=user_status, default=live)

    def __str__(self):
        return self.user.username


class UserAddress(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='address_profile')
    street = models.CharField(max_length=120, null=True)
    city = models.CharField(max_length=120, null=True)
    district = models.CharField(max_length=120, null=True)
    state = models.CharField(max_length=120, null=True)
    country = models.CharField(max_length=120, null=True)
    land_mark = models.CharField(max_length=120, null=True)
    pincode = models.CharField(max_length=120, null=True)

    def __str__(self):
        return self.user.user.username
