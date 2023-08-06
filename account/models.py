from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)

    name = models.CharField(max_length=255, default='')
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=55, default='user')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



