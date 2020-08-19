from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    display_picture = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    bio = models.CharField(max_length=140, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'
