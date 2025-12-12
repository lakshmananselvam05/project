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
        # fields = '__all__'
        exclude = ['emp_id']

class idcordform(forms.ModelForm):
    class Meta:
        model =Idcord
        # exclude = ["employee"]
        fields = "__all__"
        widgets = {
            'employee': forms.HiddenInput(),
            #  'Blood_Group': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Enter Blood Group',
            # }),

        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Emp_Attendance
        fields = '__all__'


class SalaryForm(forms.ModelForm):
    class Meta:
        model = emp_Salary
        fields = '__all__'