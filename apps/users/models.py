from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from apps.base.models import BaseModel


class User(AbstractUser, BaseModel):
     mini_bio = models.CharField(max_length=300, null=True, blank=True)
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
          elif now == self.last_login:
               ago = "hozirda online"
               return (ago)
          else:
               days = difference.days
               ago = f"{days} kun oldin"

          return f"{formatted_time} ({ago})"



class DeleteProfile(models.Model):
     user = models.OneToOneField(
          'User',
          on_delete=models.CASCADE,
          related_name='deleted_profile'
     )
     reserved_username = models.CharField(max_length=150, null=True, blank=True)
     verification_code = models.CharField(max_length=6, null=True, blank=True)
     deleted_at = models.DateTimeField(null=True, blank=True)
     code_created_at = models.DateTimeField(null=True, blank=True)

     class Meta:
          verbose_name = 'Delete Profile'
          verbose_name_plural = 'Delete Profiles'

     def delete_account(self):
          """Foydalanuvchini aktiv emas qilib belgilash va username ni o‘zgartirish"""
          self.reserved_username = self.user.username
          self.user.username = f"deleted_user_{self.user.pk}"
          self.user.is_active = False
          if hasattr(self.user, "is_deleted"):
               self.user.is_deleted = True   # agar User modelida is_deleted bo‘lsa
          self.deleted_at = timezone.now()
          self.user.save()
          self.save()

     def is_code_valid(self):
          """Tasdiqlash kodi 5 daqiqa amal qiladi"""
          if not self.code_created_at:
               return False
          return timezone.now() - self.code_created_at < timedelta(minutes=5)



import uuid
import hashlib
from datetime import timedelta
from django.db import models
from django.conf import settings
from django.utils import timezone


class PasswordResetToken(models.Model):
     """
     Foydalanuvchi parolini tiklash uchun maxsus token modeli.
     """

     user = models.ForeignKey(User,
          on_delete=models.CASCADE,
          related_name="password_reset_tokens"
     )
     token = models.CharField(
          max_length=255,
          unique=True,
          db_index=True
     )
     created_at = models.DateTimeField(auto_now_add=True)
     expires_at = models.DateTimeField()
     is_used = models.BooleanField(default=False)
     ip_address = models.GenericIPAddressField(null=True, blank=True)  # optional
     user_agent = models.TextField(null=True, blank=True)  # optional

     def save(self, *args, **kwargs):
          """
          Yangi yozuv yaratilayotganda avtomatik token va expiry vaqtini belgilaydi.
          """
          if not self.id:  # faqat yangi yozuv uchun
               raw_token = str(uuid.uuid4()) + str(uuid.uuid4())  # tasodifiy UUID
               self.token = hashlib.sha256(raw_token.encode()).hexdigest()  # DBda hash saqlaymiz
               self.expires_at = timezone.now() + timedelta(hours=1)  # 1 soat amal qiladi
          super().save(*args, **kwargs)

     def is_valid(self):
          """
          Token amal qilish muddatini va ishlatilmaganligini tekshiradi.
          """
          return not self.is_used and timezone.now() < self.expires_at

     def mark_as_used(self):
          """
          Token bir marta ishlatilgandan keyin bloklanadi.
          """
          self.is_used = True
          self.save(update_fields=["is_used"])

     def __str__(self):
          return f"Password reset token for {self.user} (valid={self.is_valid()})"
