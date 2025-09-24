from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Username",
        "id": "username",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "id": "password",
    }))


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Username",
        "id": "username",
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "placeholder": "Email",
        "id": "email",
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "id": "password1",
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password Repeat",
        "id": "password2"
    }))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')