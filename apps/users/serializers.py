from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
import re
from .models import User, DeleteProfile



class LogInUserSerializers(serializers.Serializer):
     username = serializers.CharField()
     password = serializers.CharField(write_only=True)


     def validate(self, attrs):
          username = attrs.get('username', None)
          password = attrs.get('password', None)
          
          user = authenticate(username=username, password=password)
          if not user:
               raise serializers.ValidationError({'login': 'login yoki parol xato'})
          
          attrs['user'] = user
          return attrs



class RegisterUserProfileSerializers(serializers.ModelSerializer):
     # --- BU YERDA ASOSIY QISM ---
     confirm_password = serializers.CharField(write_only=True)

     class Meta:
          model = User
          fields = [
               'id',
               'username',
               'first_name',
               'last_name',
               'email',
               'image',
               'gender',
               'phone_number',
               'birth_date',
               'password',
               'confirm_password',
          ]
          extra_kwargs = {
               'password': {'write_only': True},
          }

     def validate_username(self, value):
          if User.objects.filter(username=value).exists():
               raise serializers.ValidationError("bu username allaqchon ro'yxatdan o'tgan")
          return value

     def validate_email(self, value):
          if User.objects.filter(email=value, is_active=True, is_deleted=False).exists():
               raise serializers.ValidationError("bu email allaqchon ro'yxatdan o'tgan")
          return value

     def validate(self, attrs):
          if attrs['password'] != attrs['confirm_password']:
               raise serializers.ValidationError({"password": "Parollar bir biriga mos emas"})
          return attrs

     def create(self, validated_data):
          validated_data.pop('confirm_password')
          user = User.objects.create_user(**validated_data)
          return user



class UserProfileDataSerializers(serializers.ModelSerializer):
     formatted_last_login = serializers.SerializerMethodField()
     class Meta:
          model = User
          fields = ['id', 'username', 'first_name', 'last_name', 'mini_bio', 'email', 'image', 'phone_number', 'birth_date', 'gender', 'formatted_last_login']

     
     def get_formatted_last_login(self, obj):
          return obj.formatted_last_login if obj.last_login else "hech qachon tizimga kirmagan"



class UserProfileUpdateSerializers(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['id', 'username', 'first_name', 'last_name', 'mini_bio', 'email', 'image', 'phone_number', 'birth_date', ]

     
     def validate_username(self, value):
          if User.objects.filter(username=value).exists():
               raise serializers.ValidationError("bu username band")
          return value
     

     def validate_email(self, value):
          if User.objects.filter(email=value).exists():
               raise serializers.ValidationError("bu email band")
          return value



class DeleteProfileSerializers(serializers.ModelSerializer):
     code = serializers.CharField(write_only=True, required=True)

     class Meta:
          model = DeleteProfile
          fields = ['code']  # faqat kod kiritiladi

     def validate_code(self, value):
          profile = self.instance
          now = timezone.now()

          if not profile.verification_code:
               raise serializers.ValidationError("Tasdiqlash kodi mavjud emas.")

          if profile.verification_code != value:
               raise serializers.ValidationError("Kod noto‘g‘ri.")

          if profile.code_created_at and (now - profile.code_created_at).total_seconds() > 300:
               raise serializers.ValidationError("Kod muddati tugagan (5 daqiqa).")

          return value

     def save(self, **kwargs):
          """Agar kod to‘g‘ri bo‘lsa, foydalanuvchini o‘chiradi"""
          self.instance.delete_account()
          return self.instance



class ChangePasswordSerializers(serializers.Serializer):
     password1 = serializers.CharField(write_only=True, required=True)
     password2 = serializers.CharField(write_only=True, required=True)


     def validate_password1(self, value):
          if len(value) < 8:
               raise serializers.ValidationError("Parol kamida 8ta belgidan iborat bo'lishi kerak!")
          
          if not re.match(r'^[A-Za-z0-9_]+$', value):
               raise serializers.ValidationError("Parolda faqat lotin harflari, raqamlar va pastki chiziq bo'lishi mumkin!")
          
          return value
     

     def validate(self, attrs):
          if attrs['password1'] != attrs['password2']:
               raise serializers.ValidationError({"password": "Parollar bir biriga mos emas"})
          
          return attrs
     

     def update(self, instance, validated_data):
          instance.set_password(validated_data['password2'])
          instance.save()
          return instance



from .utils import send_password_reset_email
from .models import PasswordResetCode, User
from django.utils import timezone
from datetime import timedelta


class PasswordResetByUsernameSerializers(serializers.Serializer):
     username = serializers.CharField(required=True)

     def save(self, **kwargs):
          username = self.validated_data["username"]
          try:
               user = User.objects.get(username=username)
          except User.DoesNotExist:
               return None

          PasswordResetCode.objects.filter(user=user, is_used=False).update(is_used=True)
          token = PasswordResetCode.objects.create(user=user)
          send_password_reset_email(user)
          return token



class PasswordResetConfirmSerializers(serializers.Serializer):
     password = serializers.CharField(write_only=True, min_length=8)
     password2 = serializers.CharField(write_only=True, min_length=8)

     def validate(self, attrs):
          if attrs["password"] != attrs["password2"]:
               raise serializers.ValidationError({"password2": "Parollar bir biriga mos emas"})
          return attrs

     def save(self, token, uidb64, **kwargs):
          try:
               uid = urlsafe_base64_decode(uidb64).decode()
               user = User.objects.get(pk=uid)
               
          except (User.DoesNotExist, ValueError, TypeError, OverflowError):
               raise serializers.ValidationError({"uidb64": "Foydalanuvchi topilmadi"})

          if not default_token_generator.check_token(user, token):
               raise serializers.ValidationError({"token": "Token yaroqsiz yoki muddati o‘tgan"})


          user.set_password(self.validated_data["password"])
          user.save(update_fields=["password"])
          return user
