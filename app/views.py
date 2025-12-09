from django.shortcuts import render,redirect,HttpResponse  # pyright: ignore[reportMissingModuleSource]
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomSignupForm,EmployeeForm
from .forms import *
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
            return redirect("create-emplyoee")   
        else:
            print(user_form.errors)
            return render(request, "create.html", {"form": user_form})

    return render(request, "create.html", {"form": form})




def HR_dashborad_view(request):
    return render(request,'hr_dashboard.html')


def employee_view(request):
    emp = Employees.objects.all()
    return render(request, 'employee.html', {'emp': emp})

def emplyoee_form(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()        
            return redirect('employee')  
    else:
        form = EmployeeForm()  
    return render(request, 'create_employee_form.html', {'form': form})


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

def idcord_view(request):
    idcords=Idcord.objects.all()
    return render(request,'idcard.html',{'idcards':idcords})


from django.shortcuts import get_object_or_404

def id_cords_detalis(request, emp_id):
    emp = get_object_or_404(Employees, id=emp_id)

    # Get or create ID card for this employee
    idcard, created = Idcord.objects.get_or_create(employee=emp)

    if request.method == 'POST':
        form = idcordform(request.POST,instance=idcard)
        if form.is_valid():
            form.save()
            return redirect('idcards')
    else:
        form = idcordform(instance=idcard)

    return render(request, "id_card.html", {"form": form, "emp": emp})


def attendance_view(request):
    att=Attendance.objects.all()
    return render(request,'attendance.html',{'att':att})

def logout_view(request):
    logout(request)
    return redirect(request,"employee-login")
#--------------------------------------------------Employee Details------------------------------------------------------------

def emp_dash(request):
    return render(request, "Employee/employee_dashboard.html")

def employee_login(request):
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(user.role)
            if user.role =="hr":
                return redirect("hr_dashboard")
            else:
            
                return redirect("emp_dashboard")

        else:
            return render(request, "Employee/emp_login.html", {"error": "Invalid credentials"})
    return render(request, "Employee/emp_login.html")   

def dashborad_view(request):
    return render(request,'Employee/employee_dashboard.html')

from datetime import datetime
from datetime import datetime
from django.shortcuts import render, redirect
from .models import Employees, Attendance

def employee_attendance_view(request):
    emp = Employees.objects.get(user=request.user)

    now = datetime.now()
    today_date = now.date()
    time_now = now.time().strftime("%H:%M:%S")

    if request.method == "POST":
        action = request.POST.get("action")

        attendance, created = Attendance.objects.get_or_create(
            employees=emp,
            date=today_date,
            defaults={"status": "present"}
        )

        if action == "login" and created:
            attendance.check_in = now.time()
            attendance.save()

        elif action == "logout":
            attendance.check_out = now.time()
            attendance.save()

        return redirect("emp_dashboard")

    return render(request,"Employee/emp_attendance.html",{"today": today_date, "current_time": time_now})


def id_card_view(request):
    user = request.user

    # If employee doesn't exist → emp = None
    emp = Employees.objects.filter(user=user).first()

    if not emp:
        return render(request, "Employee/id_card.html", {"id_details": None})

    id_details = Idcord.objects.filter(employee=emp)

    return render(request, "Employee/id_card.html", {"id_details": id_details})




