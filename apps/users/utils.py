from django.core.mail import send_mail
from django.conf import settings

def send_delete_code_email(to_email, code):
     subject = "Profilni o‘chirish uchun tasdiqlash kodi"
     message = f"Sizning tasdiqlash kodingiz: {code}\nBu kod 5 daqiqa davomida amal qiladi.\nEslatma: bu hisobni o'chirib tashlashasangiz barcha ma'lumotlaringiz yo'qoladi va qayta tiklab bo'lmaydi."
     from_email = settings.DEFAULT_FROM_EMAIL
     recipient_list = [to_email]

     send_mail(subject, message, from_email, recipient_list)





# reset password
import secrets
import hashlib
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from .models import PasswordResetToken


def generate_password_reset_token(user, ip_address=None, user_agent=None):
     """
     Foydalanuvchi uchun parolni tiklash tokenini yaratadi va DB’da saqlaydi.
     """

     # Avval eski tokenlarni bekor qilish
     PasswordResetToken.objects.filter(user=user, is_used=False).update(is_used=True)

     # Tasodifiy token yaratamiz
     raw_token = secrets.token_urlsafe(48)  # foydalanuvchiga yuboriladigan token
     hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()

     # Yangi token obyektini yaratamiz
     reset_token = PasswordResetToken.objects.create(
          user=user,
          token=hashed_token,
          expires_at=timezone.now() + timedelta(hours=1),  # 1 soat amal qiladi
          ip_address=ip_address,
          user_agent=user_agent
     )

     return raw_token, reset_token


def send_password_reset_email(user, raw_token):
     """
     Foydalanuvchiga parolni tiklash emailini yuboradi.
     """
     reset_link = f"http://127.0.0.1:8000/reset-password?token={raw_token}"  # front link

     subject = "Parolni tiklash"
     message = f"Salom, {user.username}!\n\nParolingizni tiklash uchun quyidagi linkga bosing:\n{reset_link}\n\nAgar siz so‘ramagan bo‘lsangiz, bu xabarni e’tiborsiz qoldiring."
     
     send_mail(
          subject,
          message,
          settings.DEFAULT_FROM_EMAIL,
          [user.email],
          fail_silently=False,
     )
