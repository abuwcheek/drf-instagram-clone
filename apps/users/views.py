from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import logout
from django.utils import timezone
import random

from conf import settings
from .models import  User, DeleteProfile
from .utils import send_delete_code_email, send_password_reset_email
from .serializers import (LogInUserSerializers, RegisterUserProfileSerializers, 
                         UserProfileDataSerializers,UserProfileUpdateSerializers,
                         DeleteProfileSerializers, ChangePasswordSerializers,
                         PasswordResetByUsernameSerializers, PasswordResetConfirmSerializers,)




class LogInUserView(APIView):
     permission_classes = [AllowAny]

     def post(self, request):
          serializer = LogInUserSerializers(data=request.data)
          serializer.is_valid(raise_exception=True)
          user = serializer.validated_data['user']

          
          # Foydalanuvchi uchun JWT token yaratish
          refresh = RefreshToken.for_user(user)

          data = {
               'status': True,
               'message': "tizimga muvaffaqiyatli kirdingiz",
               'data': {
                    'username': user.username,
                    'email': user.email,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'created_at': user.created_at
               }
          }
          return Response(data=data)



class LogoutUserView(APIView):
     permission_classes = [IsAuthenticated]

     def post(self, request):
          tokens = OutstandingToken.objects.filter(user=request.user)
          for token in tokens:
               BlacklistedToken.objects.get_or_create(token=token)
          data = {
               'status': True,
               'message': "tizimdan muvaffaqiyatli chiqdingiz"
          }
          return Response(data=data)



class RegisterUserProfileView(APIView):
     permission_classes = [AllowAny]

     def post(self, request):
          try:
               username = request.user.username
               email = request.user.email

               if User.objects.filter(username=username).exists():
                    data = {
                         'status': False,
                         'message': "bu username orqali ro'yxatdan o'tilgan"
                    }
                    return Response(data=data)
               
               if User.objects.filter(email=email).exists():
                    data = {
                         'status': False,
                         'message': "bu email orqali ro'yxatdan o'tilgan"
                    }

          except Exception as e:
               pass

          serializer = RegisterUserProfileSerializers(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()

          data = {
               'status': True,
               'message': "muvaffaqqiyatli ro'yxatdan o'tdingiz",
               'data': serializer.data
          }

          return Response(data=data)
     


class UserProfileDataView(APIView):
     permission_classes = [IsAuthenticated]
     def get(self, request):
          user = get_object_or_404(User, username=request.user.username, email=request.user.email)
          serializers = UserProfileDataSerializers(user, context={'request': request})

          data = {
               'status': True,
               'message': "salom, biz sizning shaxsiy sahifangizdamiz",
               'data': serializers.data
          }
          return Response(data=data)



class UserProfileUpdateView(APIView):
     permission_classes = [IsAuthenticated]

     def patch(self, request):
          user = get_object_or_404(User, username=request.user.username, email=request.user.email)
          serializer = UserProfileUpdateSerializers(user, data=request.data, partial=True, context={'request': request})

          if serializer.is_valid(raise_exception=True):
               serializer.save()

               data = {
                    'status': True,
                    'message': "ma'lumotlar yangilandi",
                    'data': serializer.data
               }
               return Response(data=data)
          
          data = {
               'status': False,
               'message': "xatolik yuz berdi",
               'data': serializer.errors
          }
          return Response(data=data)



class RequestDeleteProfileView(APIView):
     """Foydalanuvchiga profilni o‘chirish uchun kod yuborish"""
     permission_classes = [IsAuthenticated]

     def post(self, request):
          user = request.user
          delete_profile, created = DeleteProfile.objects.get_or_create(user=user)

          # 6 xonali kod generatsiya qilamiz
          code = str(random.randint(100000, 999999))
          delete_profile.verification_code = code
          delete_profile.code_created_at = timezone.now()
          delete_profile.save()

          # Email orqali yuboramiz
          send_delete_code_email(user.email, code)

          data = {
               "message": "Profilni o‘chirish uchun kod emailingizga yuborildi.",
               "email": user.email
          }
          return Response(data=data)



class DeleteProfileUserView(APIView):
     """Foydalanuvchi kod yuborib profilini o‘chiradi"""
     permission_classes = [IsAuthenticated]

     def post(self, request):
          try:
               delete_profile = request.user.deleted_profile
          except DeleteProfile.DoesNotExist:
               data = {
                    "message": "Profil o‘chirish uchun so‘rov yuborilmagan."
               }
               return Response(data=data)

          serializer = DeleteProfileSerializers(
               instance=delete_profile,
               data=request.data,
               context={'request': request}
          )

          if serializer.is_valid():
               serializer.save()
               data = {
                    "message": "Profilingiz muvaffaqiyatli o‘chirildi.",
                    'username': serializer.user.username,
                    'email': serializer.user.email
               }
               return Response(data=data)
          return Response(data=serializer.errors)




# change password
class ChangePasswordView(APIView):
     permission_classes = [IsAuthenticated]


     def put(self, request, *args, **kwargs):
          user = request.user
          serializer = ChangePasswordSerializers(data=request.data, instance=user)

          if serializer.is_valid(raise_exception=True):
               serializer.save()
               data = {
                    'status': True,
                    'message': "Parol muvaffaqiyatli yangilandi",
               }
               return Response(data=data)
          
          data = {
               'status': False,
               'message': "Xatolik yuz berdi",
               'data': serializer.errors
          }
          return Response(data=data)




# password reset
class PasswordResetByUsernameView(APIView):
     permission_classes = [AllowAny]

     def post(self, request, *args, **kwargs):
          serializer = PasswordResetByUsernameSerializers(data=request.data)
          serializer.is_valid(raise_exception=True)
          user = serializer.save()

          username = serializer.validated_data['username']
          try:
               user = User.objects.get(username=username)
               email = user.email

               # reset email yuborish
               send_password_reset_email(user)   # utils ichida function
               data = {
                    'status': True,
                    'message': f"Agar {username} foydalanuvchisi mavjud bo‘lsa",
                    'email': f"Havola {email} manziliga yuborildi."
               }
          except User.DoesNotExist:
               data = {
                    'status': False,
                    'message': "Bunday foydalanuvchi mavjud emas."
               }

          return Response(data=data)



class PasswordResetConfirmView(APIView):
     permission_classes = [AllowAny]

     def post(self, request, uidb64, token, *args, **kwargs):
          serializer = PasswordResetConfirmSerializers(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save(token=token, uidb64=uidb64)

          data = {
               'status': True,
               'message': "Parol muvaffaqiyatli yangilandi."
          }
          return Response(data=data)
