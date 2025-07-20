from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
     list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'gender', 'birth_date', 'phone_number', 'created_at', 'updated_at', 'password', 'is_staff', 'is_active', 'is_deleted', 'is_archived', 'is_featured', 'is_verified', 'is_published')
     list_display_links = ('id', 'username', 'email', 'first_name', 'last_name',)
     list_editable = ( 'is_staff', 'is_active', 'is_deleted', 'is_archived', 'is_featured', 'is_verified', 'is_published')
     list_filter = ('id', 'username', 'email', 'birth_date', 'gender', 'created_at', 'is_active')