from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from user.managers import UserManager

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
)

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=70,unique=True)
    phone_number = models.IntegerField(verbose_name="Phone Number", unique=True, blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']


    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = "Users"

