from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User



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
          if User.objects.filter(email=value).exists():
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
          fields = ['id', 'username', 'first_name', 'last_name', 'email', 'image', 'phone_number', 'birth_date', 'gender', 'formatted_last_login']

     
     def get_formatted_last_login(self, obj):
          return obj.formatted_last_login if obj.last_login else "Hech qachon tizimga kirmagan"



class UserProfileUpdateSerializers(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['id', 'username', 'first_name', 'last_name', 'email', 'image', 'phone_number', 'birth_date', ]

     
     def validate_username(self, value):
          if User.objects.filter(username=value).exists():
               raise serializers.ValidationError("bu username band")
          return value
     

     def validate_email(self, value):
          if User.objects.filter(email=value).exists():
               raise serializers.ValidationError("bu email band")
          return value