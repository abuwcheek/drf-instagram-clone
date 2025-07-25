from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.base.models import BaseModel


class User(AbstractUser, BaseModel):
     GENDER_CHOICES = [
          ('JINSI', 'Jinsi'),
          ('ERKAK', 'Erkak'),
          ('AYOL', 'Ayol'),
     ]

     gender = models.CharField(
          max_length=10,
          choices=GENDER_CHOICES,
          default='ERKAK',
          blank=True,
          null=True
     )
     image = models.ImageField(
          upload_to='users/images/', null=True, blank=True
     )
     birth_date = models.DateField(null=True, blank=True)
     email = models.EmailField(unique=True)
     phone_number = models.CharField(max_length=15)


     def __str__(self):
          return self.username