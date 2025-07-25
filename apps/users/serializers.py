from rest_framework import serializers
from .models import User

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
