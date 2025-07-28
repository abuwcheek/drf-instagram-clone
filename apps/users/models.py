from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
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
          default='JINSI',
          blank=True,
          null=True
     )
     image = models.ImageField(
          upload_to='users/images/', null=True, blank=True
     )
     birth_date = models.DateField(null=True, blank=True)
     email = models.EmailField(unique=True)
     phone_number = models.CharField(max_length=15)
     mini_bio = models.CharField(max_length=300, null=True, blank=True)


     def __str__(self):
          return self.username
     

     @property
     def formatted_last_login(self):
          if not self.last_login:
               return "Hech qachon tizimga kirmagan"

          # Kun, oy, yil va vaqt formatlash
          formatted_time = self.last_login.strftime("%d-%m-%Y %H:%M:%S")

          # Qancha vaqt oldinligini hisoblash
          now = timezone.now()
          difference = now - self.last_login

          # Masofani odamga oson o‘qiladigan qilib
          if difference < timedelta(minutes=1):
               ago = "bir necha soniya oldin"
          elif difference < timedelta(hours=1):
               minutes = int(difference.total_seconds() / 60)
               ago = f"{minutes} daqiqa oldin"
          elif difference < timedelta(days=1):
               hours = int(difference.total_seconds() / 3600)
               ago = f"{hours} soat oldin"
          else:
               days = difference.days
               ago = f"{days} kun oldin"

          return f"{formatted_time} ({ago})"



class DeleteProfile(User, BaseModel):
     deleted_at = models.DateTimeField(null=True, blank=True)
     reserved_username = models.CharField(max_length=150, null=True, blank=True)
     verification_code = models.CharField(max_length=6, null=True, blank=True)

     def delete_account(self):
          # Username ni band qilib qo'yish
          self.reserved_username = self.username
          self.username = f"deleted_user_{self.pk}"
          self.is_deleted = True
          self.deleted_at = timezone.now()
          self.save()