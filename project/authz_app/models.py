from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя с уникальными именами для обратных связей
    """
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='группы',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_groups',  # Уникальное имя обратной связи
        related_query_name='customuser_group',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='разрешения пользователя',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_perms',  # Уникальное имя обратной связи
        related_query_name='customuser_perm',
    )

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
