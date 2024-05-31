# coding=windows-1251
from django import forms
from django.core.exceptions import ValidationError
from .models import *


class UserLoginForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': '�����'}), label='�����')
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '������'}), label='������')


