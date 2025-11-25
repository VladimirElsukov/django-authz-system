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

class LoginForm(forms.Form):
    """
    Русскоязычная форма входа, принимающая email вместо username.
    """
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autofocus': True}),
        help_text=_("Введите ваш email."),
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

    def __init__(self, request=None, *args, **kwargs):
        self.request = request  # Сохраняем request
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        Очистка данных формы.
        """
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Неправильные email или пароль."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("Этот аккаунт отключён."))

        return cleaned_data

    def get_user(self):
        return self.user_cache

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
        }