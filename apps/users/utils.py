from django.core.mail import send_mail
from django.conf import settings

def send_delete_code_email(to_email, code):
     subject = "Profilni o‘chirish uchun tasdiqlash kodi"
     message = f"Sizning tasdiqlash kodingiz: {code}\nBu kod 5 daqiqa davomida amal qiladi.\nEslatma: bu hisobni o'chirib tashlashasangiz barcha ma'lumotlaringiz yo'qoladi va qayta tiklab bo'lmaydi."
     from_email = settings.DEFAULT_FROM_EMAIL
     recipient_list = [to_email]

     send_mail(subject, message, from_email, recipient_list)
