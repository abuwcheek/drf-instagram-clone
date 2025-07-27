from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import User
from .serializers import RegisterUserProfileSerializers, UserProfileDataSerializers




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