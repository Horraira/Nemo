from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class MainUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class appUserForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['age', 'phone', 'address']


class AdminForm(forms.ModelForm):
    class Meta:
        model = AdminUser
        fields = ['designation', 'age', 'phone', 'address']
