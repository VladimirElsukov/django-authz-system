from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import success, error
from .forms import RegistrationForm, LoginForm, ProfileEditForm
from rest_framework import generics
from .models import Role, Permission
from .serializers import RoleSerializer, PermissionSerializer
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import requires_role


def index_view(request):
    return render(request, 'index.html')


@requires_role('admin')
def some_admin_action(request):
    # Здесь выполняем административные операции
    pass

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("Форма регистрации валидна:", form.cleaned_data)
            user = form.save(commit=False)
            user.username = user.email  # Устанавливаем username равным email
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, _("Вы успешно зарегистрированы!"))
            return redirect('authz:login')
        else:
            print("Форма регистрации невалидна:", form.errors)
    else:
        form = RegistrationForm()
    return render(request, 'authz_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)  # Передаёшь request в форму
        if form.is_valid():
            print("Форма входа валидна:", form.cleaned_data)
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, _("Вы успешно вошли в систему!"))
                return redirect('authz:profile')
            else:
                print("Пользователь не найден:", form.cleaned_data)
                messages.error(request, _("Пользователь не найден."))
        else:
            print("Форма входа невалидна:", form.errors)
            messages.error(request, _("Неверные имя пользователя или пароль."))
    else:
        form = LoginForm(request)  # Передаёшь request в форму
    return render(request, 'authz_app/login.html', {'form': form})



def logout_view(request):
    logout(request)
    success(request, _("Вы успешно вышли из системы."))
    return redirect('authz:login')

def profile_view(request):
    return render(request, 'authz_app/profile.html')

class RoleList(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class PermissionList(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


@require_http_methods(['GET'])
def profile_view(request):
    context = {
        'user': request.user,
        'message': 'Приветствуем Администратора!',
    }
    return render(request, 'authz_app/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('authz:profile')
    else:
        form = ProfileEditForm(instance=user)
    return render(request, 'authz_app/edit_profile.html', {'form': form})


@login_required
def deactivate_account(request):
    if request.method == 'POST':
        user = request.user
        user.is_active = False  # Делаем пользователя неактивным
        user.save()

        # Устанавливаем сообщение
        messages.success(request, 'Ваш аккаунт был успешно удалён.')

        # Сначала возвращаемся на страницу подтверждения
        return render(request, 'authz_app/deactivated_confirmation.html')
    return render(request, 'authz_app/deactivate_account.html')