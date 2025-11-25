from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods



class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя с уникальными именами для обратных связей
    """
    # ====> Ленивая связь с группами и разрешениями (используем уникальные имена):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='группы',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_groups',  # Имя для обратной связи с группой
        related_query_name='customuser_group',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='разрешения пользователя',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_perms',  # Имя для обратной связи с разрешением
        related_query_name='customuser_perm',
    )

    # ====> Своя связь с ролями:
    roles = models.ManyToManyField('authz_app.Role', related_name='users_with_role', blank=True)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def has_role(self, role_name):
        """Проверяет, принадлежит ли пользователь указанной роли"""
        return self.roles.filter(name=role_name).exists()

    def assign_role(self, role_name):
        """Назначает пользователю указанную роль."""
        try:
            role = Role.objects.get(name=role_name)
            self.roles.add(role)
        except Role.DoesNotExist:
            print(f"Ошибка: роль '{role_name}' не существует.")

    def remove_role(self, role_name):
        """Удаляет роль у пользователя."""
        try:
            role = Role.objects.get(name=role_name)
            self.roles.remove(role)
        except Role.DoesNotExist:
            print(f"Ошибка: роль '{role_name}' не существует.")

    def delete(self, using=None, keep_parents=False):
        """Осуществляет мягкое удаление пользователя."""
        self.is_active = False
        self.save()

class RoleManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Role(models.Model):
    objects = RoleManager()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Permission(models.Model):
    """
    Модель разрешений
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    resource = models.CharField(max_length=100)
    action = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.role}: {self.resource}/{self.action}'


@require_http_methods(['GET'])
def profile_view(request):
    context = {
        'user': request.user,
        'message': 'Приветствуем Администратора!',
    }
    return render(request, 'authz_app/profile.html', context)