from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from profiles.models import Profile

UserModel = get_user_model()


class UpdateProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ("is_verified","is_complete", "user", "money",)


class UpdateProfileMoney(ModelForm):
    class Meta:
        model = Profile
        fields = ('money',)


