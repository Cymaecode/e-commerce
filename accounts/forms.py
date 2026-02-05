from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required = True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "phone", "address")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "phone", "address")

