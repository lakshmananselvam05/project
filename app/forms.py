from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class CustomSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username","email","role"]
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }
        
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = '__all__'
