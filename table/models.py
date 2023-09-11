from django.db import models
from django.contrib.auth.models import AbstractUser
class signup(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    CompanyName = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    email = models.EmailField(max_length=255)
   