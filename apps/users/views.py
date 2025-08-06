from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
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
from .utils import generate_verification_code
from .serializers import (LogInUserSerializers, RegisterUserProfileSerializers, 
                         UserProfileDataSerializers,UserProfileUpdateSerializers,
                         DeleteProfileSerializers)




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
               'message': "salom, biz sizning sahifangizdamiz",
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
     permission_classes = [IsAuthenticated]

     def post(self, request):
          user = request.user
          delete_profile, _ = DeleteProfile.objects.get_or_create(user=user)

          code, timestamp = generate_verification_code()
          delete_profile.verification_code = code
          delete_profile.code_created_at = timestamp
          delete_profile.save()

          send_mail(
               subject="Instagram profil o‘chirish kodi",
               message=f"Sizning tasdiq kodingiz: {code}\n\nKodingiz 5 daqiqa ichida amal qiladi.\n\n"
                         f"Eslatma: agar bu hisobni o‘chirsangiz, qayta kira olmaysiz!",
               from_email=settings.DEFAULT_FROM_EMAIL,
               recipient_list=[user.email],
               fail_silently=False,
          )

          return Response({
               "status": True,
               "message": "Tasdiqlash kodi emailga yuborildi"
          })



class DeleteProfileView(APIView):
     permission_classes = [IsAuthenticated]

     def post(self, request):
          user = request.user
          try:
               delete_profile = user.deleted_profile
          except DeleteProfile.DoesNotExist:
               data = {
                    "status": False,
                    "message": "Avval tasdiqlash kodini oling."
               }
               return Response(data=data)

          serializer = DeleteProfileSerializers(
               delete_profile,
               data=request.data,
               context={'request': request},
               partial=True
          )
          if serializer.is_valid():
               serializer.save()
               data = {
                    'status': True,
                    'message': "Hisob muvaffaqiyatli o‘chirildi",
                    'data': serializer.data
               }
               return Response(data=data)
          return Response(serializer.errors, status=400)
