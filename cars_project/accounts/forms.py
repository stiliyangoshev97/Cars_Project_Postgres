from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

UserModel = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("email",)

    def get_clean_password(self):
        return self.cleaned_data['password1']


class LoginForm(AuthenticationForm):
    user = None

    password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput()
    )

