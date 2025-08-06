from django.contrib import admin
from .models import User, DeleteProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
     list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'gender', 'birth_date', 'phone_number', 'created_at', 'updated_at', 'is_staff', 'is_active', 'is_deleted', 'is_archived', 'is_featured', 'is_verified', 'is_published')
     list_display_links = ('id', 'username', 'email', 'first_name', 'last_name',)
     list_editable = ( 'is_staff', 'is_active', 'is_deleted', 'is_archived', 'is_featured', 'is_verified', 'is_published')
     list_filter = ('id', 'username', 'email', 'birth_date', 'gender', 'created_at', 'is_active')



@admin.register(DeleteProfile)
class DeleteProfileAdmin(admin.ModelAdmin):
     list_display = ('id', 'user', 'reserved_username', 'verification_code', 'code_created_at', 'deleted_at')
     list_display_links = ('id', 'user', 'reserved_username', 'verification_code',)
     list_filter = ('id', 'user', 'reserved_username', 'deleted_at')
     