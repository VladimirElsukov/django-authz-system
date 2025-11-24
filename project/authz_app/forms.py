from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import CustomUser
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _



class RegistrationForm(forms.ModelForm):
    password_confirm = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput(),
        help_text=_("Введите пароль еще раз для подтверждения."),
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password')
        labels = {
            'first_name': _("Имя"),
            'last_name': _("Фамилия"),
            'email': _("Электронная почта"),
            'password': _("Пароль"),
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError(_("Пароли не совпадают!"))

        return cleaned_data


class LoginForm(AuthenticationForm):
    """
    Русскоязычная форма входа.
    """
    username = forms.CharField(
        label=_("Имя пользователя или электронная почта"),
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True}),
        help_text=_("Введите ваше имя пользователя или электронную почту."),
    )

    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        help_text=_("Введите ваш пароль."),
    )

    remember_me = forms.BooleanField(
        label=_("Запомнить меня?"),
        required=False,
        initial=True,
    )

    def confirm_login_allowed(self, user):
        """
        Добавляет дополнительную проверку перед авторизацией.
        """
        if not user.is_active:
            raise forms.ValidationError(_("Этот аккаунт отключён."), code="inactive")

    def clean(self):
        """
        Очистка данных формы.
        """
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Неправильное имя пользователя или пароль."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("Этот аккаунт отключён."))

        return cleaned_data
