from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import success, error
from .forms import RegistrationForm, LoginForm
from rest_framework import generics
from .models import Role, Permission
from .serializers import RoleSerializer, PermissionSerializer
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods




def index_view(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            success(request, _("Вы успешно зарегистрированы!"))
            return redirect('authz:login')
    else:
        form = RegistrationForm()
    return render(request, 'authz_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            success(request, _("Вы успешно вошли в систему!"))
            return redirect('authz:profile')
        else:
            error(request, _("Неверные имя пользователя или пароль."))
    else:
        form = LoginForm()
    return render(request, 'authz_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    success(request, _("Вы успешно вышли из системы."))
    return redirect('authz:login')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('authz:login')
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