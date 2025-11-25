from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя с уникальными именами для обратных связей
    """
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'  # Используем email как средство аутентификации
    REQUIRED_FIELDS = []  # Не нужно требовать обязательных полей кроме email

    # Связь с ролями
    roles = models.ManyToManyField('authz_app.Role', related_name='users_with_role', blank=True)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Должно присутствовать для разграничения полномочий
    is_superuser = models.BooleanField(default=False)  # Должно присутствовать для разграничения полномочий

    # Группы и разрешения
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('группы'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='customuser_groups',  # Новое имя для обратной связи
        related_query_name='customuser_group',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('разрешения пользователя'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='customuser_perms',  # Новое имя для обратной связи
        related_query_name='customuser_perm',
    )

    objects = CustomUserManager()  # Менеджер для новой модели пользователя

    def has_role(self, role_name):
        """Проверяет, принадлежит ли пользователь указанной роли"""
        return self.roles.filter(name=role_name).exists()

    def assign_role(self, role_name):
        """Назначает пользователю указанную роль."""
        try:
            role = Role.objects.get(name=role_name)
            self.roles.add(role)
            print(f"Успешно назначила роль '{role_name}'.")
        except Role.DoesNotExist:
            print(f"Ошибка: роль '{role_name}' не существует.")

    def remove_role(self, role_name):
        """Удаляет роль у пользователя."""
        try:
            role = Role.objects.get(name=role_name)
            self.roles.remove(role)
            print(f"Успешно удалил роль '{role_name}'.")
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