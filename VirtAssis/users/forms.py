from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput({'class': 'form-control'}))
    email = forms.CharField(max_length=100,
                            required=True,
                            widget=forms.TextInput())
    password1 = forms.CharField(max_length=50, min_length=5, required=True,
                                widget=forms.PasswordInput({'class': 'form-control'}))
    password2 = forms.CharField(max_length=50, min_length=5, required=True,
                                widget=forms.PasswordInput({'class': 'form-control'}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput({'class': 'form-control'}))
    password = forms.CharField(max_length=50, min_length=5, required=True,
                               widget=forms.PasswordInput({'class': 'form-control'}))

    class Meta:
        model = User
        fields = ["username", "password"]
