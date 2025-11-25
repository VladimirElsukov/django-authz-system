# admin.py
from django.contrib import admin
from .models import CustomUser, Role, Permission

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    filter_horizontal = ('roles',)  # Горизонтальный выбор ролей

class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'resource', 'action']
    search_fields = ['role__name', 'resource', 'action']

# Регистрируем модели с нашими настройками
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Permission, PermissionAdmin)