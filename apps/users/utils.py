from django.core.mail import send_mail
from django.conf import settings

def send_delete_code_email(to_email, code):
     subject = "Profilni o‘chirish uchun tasdiqlash kodi"
     message = f"Sizning tasdiqlash kodingiz: {code}\nBu kod 5 daqiqa davomida amal qiladi.\nEslatma: bu hisobni o'chirib tashlashasangiz barcha ma'lumotlaringiz yo'qoladi va qayta tiklab bo'lmaydi."
     from_email = settings.DEFAULT_FROM_EMAIL
     recipient_list = [to_email]

     send_mail(subject, message, from_email, recipient_list)



from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator



def send_password_reset_email(user):
     # foydalanuvchi ID sini kodlash
     uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
     # parol tiklash token generatsiya qilish
     token = default_token_generator.make_token(user)

     # reset qilish havolasi (API endpoint)
     reset_link = f"http://127.0.0.1:8000/user/password-reset/confirm/{uidb64}/{token}/"

     subject = "Parolni tiklash"
     message = f"Quyidagi API havola orqali parolingizni qayta o‘rnating:\n\n{reset_link}"
     from_email = settings.DEFAULT_FROM_EMAIL

     # email yuborish
     send_mail(
          subject,
          message,
          from_email,
          [user.email],
          fail_silently=False,
     )
