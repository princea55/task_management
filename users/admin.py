from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


# Customize User model registration if needed
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')  # Display relevant fields in the admin list
    search_fields = ('username', 'email')  # Add search functionality
