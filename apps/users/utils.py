import random
from django.utils import timezone

def generate_verification_code():
     """6 xonali random kod va hozirgi vaqtni qaytaradi"""
     code = str(random.randint(100000, 999999))
     timestamp = timezone.now()
     return code, timestamp
