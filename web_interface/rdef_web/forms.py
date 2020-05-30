# rdef_web/forms.py
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from rdef_web.models import UserProfileInfo
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'type': 'text', 'id': 'username', 'placeholder': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'type': 'password', 'id': 'password', 'placeholder': 'password'}))


class UserForm(forms.ModelForm):
    username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(
        attrs={'class': 'mdl-textfield__input', 'type': 'text', 'id': 'username', 'placeholder': 'username'}))

    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'type': 'password', 'id': 'password', 'placeholder': 'password'}))

    password_confirm = forms.CharField(label="Password", max_length=30,
                                       widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'type': 'password', 'id': 'password_confirm', 'placeholder': 'confirm password'}))

    email = forms.EmailField(label="Email", max_length=60, widget=forms.TextInput(
        attrs={'class': 'mdl-textfield__input', 'type': 'text', 'id': 'email', 'placeholder': 'email'}))

    class Meta():
        model = User
        fields = ('username', 'password', 'email')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')
