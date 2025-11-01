from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class AdminUser(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Role", {"fields": ("role", "full_name")}),)
    list_display = ("username", "email", "role", "is_active", "is_staff")
