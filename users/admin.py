from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'username', 'is_staff', 'is_active', 'is_blocked')
    search_fields = ('email', 'username', 'phone')
    ordering = ('email',)
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('avatar', 'phone', 'country', 'is_blocked')}),
    )
