from django.shortcuts import render,redirect,HttpResponse  # pyright: ignore[reportMissingModuleSource]
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomSignupForm,EmployeeForm

from .models import *
# Create your views here.
def signup_view(request):
    form = CustomSignupForm()
    for field in form.fields.values():
        field.help_text = ""
    if request.method == "POST":
        user_form = CustomSignupForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            # login(request, user)
            return redirect("employee")   
        else:
            print(user_form.errors)
            return render(request, "create.html", {"form": user_form})

    return render(request, "create.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(user.role)
            if user.role =="HR":
                return redirect("hr_dashboard")
            else:
            
                return redirect("emp_dashboard")

        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")   

def dashborad_view(request):
    return render(request,'employee_dashboard.html')

def HR_dashborad_view(request):
    # form=EmployeeForm()
    # if request.method=="POST":
    #     form=EmployeeForm(request.POST,request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('hr_dasbhoard')
    return render(request,'hr_dashboard.html')


def employee_view(request):
    emp=Employees.objects.all()
    form=EmployeeForm()
    if request.method=='POST':
        form=EmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee')
    return render(request,'employee.html',{'emp':emp,"form":form})

def emlployee_edit_view(request,id):
    emp=Employees.objects.get(id=id)
    form=EmployeeForm(instance=emp)
    if request.method=='POST':
        form=EmployeeForm(request.POST,request.FILES,instance=emp)
        if form.is_valid():
            form.save()
            return redirect('employee')
    return render(request,'employee_edit.html',{'form':form})

def employee_delete_view(request,id):
    emp=Employees.objects.get(id=id)
    emp.delete()
    return redirect('employee')

