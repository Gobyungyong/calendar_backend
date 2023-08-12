from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            None,
            {"fields": ("username", "password", "is_active")},
        ),
        (("Personal info"), {"fields": ("email",)}),
    )

    list_display = ("username", "password", "email", "name")
