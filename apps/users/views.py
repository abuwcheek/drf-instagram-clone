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

from conf import settings
from .models import User
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
          code = generate_verification_code()
          user.verification_code = code
          user.save()

          # Email yuborish
          send_mail(
               subject="Profil o'chirish tasdiq kodi",
               message=f"Sizning tasdiq kodingiz: {code}",
               from_email=settings.DEFAULT_FROM_EMAIL,
               recipient_list=[user.email],
               fail_silently=False,
          )

          data = {
               "status": True,
               "message": "tasdiq kodi emailga yuborildi."
          }
          return Response(data=data)



class DeleteAccountView(APIView):
     permission_classes = [IsAuthenticated]

     def post(self, request):
          serializer = DeleteProfileSerializers(data=request.data, context={'request': request})
          if serializer.is_valid():
               serializer.save()
               data = {
                    'status': True,
                    'message': "profil o‘chirildi.",
                    'data': serializer.data
               }
               return Response(data=data)
          return Response(serializer.errors)
