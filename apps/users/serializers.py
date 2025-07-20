from rest_framework import serializers
from .models import User


class RegisterUserProfileSerializers(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['id', 'username', 'first_name', 'last_name', 'email', 'image', 'gender', 'phone_number', 'birth_date', 'password', 'confirm_password']