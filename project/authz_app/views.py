from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm

def register_view(request):
    # Нет требований к роли для регистрации
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('authz:login')
    context = {'form': form}
    return render(request, 'authz_app/register.html', context)

def login_view(request):
    # Доступ разрешен любому пользователю
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('authz:profile')
    return render(request, 'authz_app/login.html')

def logout_view(request):
    # Выход возможен без проверки ролей
    logout(request)
    return redirect('authz:login')

def profile_view(request):
    # Необходима проверка роли для доступа к профилю
    profile_view.required_role = 'authenticated'  # Нужна любая роль, кроме анонимной
    return render(request, 'authz_app/profile.html')

def has_role(self, role_name):
    roles = self.roles.values_list('name', flat=True)
    return role_name in roles