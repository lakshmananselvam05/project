from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Employees, Idcord, Emp_Attendance, emp_Salary


class CustomSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
        for field in self.fields.values():
            field.help_text = ""


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ['user', 'name', 'Gender', 'phone', 'depertment', 'designation', 'salary', 'photo']
        widgets = {
            'user':        forms.Select(attrs={'class': 'form-control'}),
            'name':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'Gender':      forms.Select(attrs={'class': 'form-control'}),
            'phone':       forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'depertment':  forms.Select(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Designation'}),
            'salary':      forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly Salary'}),
            'photo':       forms.FileInput(attrs={'class': 'form-control'}),
        }


class idcordform(forms.ModelForm):
    class Meta:
        model = Idcord
        fields = ['address', 'Blood_Group', 'DOB', 'Emergency_contact_No']
        widgets = {
            'address':              forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Address'}),
            'Blood_Group':          forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. A+'}),
            'DOB':                  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DD-MM-YYYY'}),
            'Emergency_contact_No': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Contact'}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Emp_Attendance
        fields = ['employee', 'date', 'status', 'check_in', 'check_out', 'total_hours']
        widgets = {
            'employee':   forms.Select(attrs={'class': 'form-control'}),
            'date':       forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status':     forms.Select(attrs={'class': 'form-control'}),
            'check_in':   forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'check_out':  forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'total_hours':forms.NumberInput(attrs={'class': 'form-control'}),
        }


class SalaryForm(forms.ModelForm):
    class Meta:
        model = emp_Salary
        fields = ['employee', 'month', 'year', 'present_days', 'salary']
        widgets = {
            'employee':    forms.Select(attrs={'class': 'form-control'}),
            'month':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. January'}),
            'year':        forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2026'}),
            'present_days':forms.NumberInput(attrs={'class': 'form-control'}),
            'salary':      forms.NumberInput(attrs={'class': 'form-control'}),
        }