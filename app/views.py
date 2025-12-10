from django.shortcuts import render,redirect,HttpResponse  # pyright: ignore[reportMissingModuleSource]
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomSignupForm,EmployeeForm
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
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
            return redirect("create-employee")   
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
    att=Emp_Attendance.objects.all()
    return render(request,'attendance.html',{'att':att})


from django.shortcuts import render
from django.db.models import Q
from datetime import datetime
from .models import Employees, Emp_Attendance


def hr_attendance_panel(request):
    employees = Employees.objects.all()

    # ----- FILTER INPUTS -----
    month = request.GET.get("month")
    department = request.GET.get("department")
    emp_id = request.GET.get("employee")

    attendance = Emp_Attendance.objects.all().order_by("-date")

    # ----- APPLY FILTERS -----
    if month:
        year, mon = month.split("-")
        attendance = attendance.filter(date__year=year, date__month=mon)

    if department:
        attendance = attendance.filter(employee__depertment=department)

    if emp_id:
        attendance = attendance.filter(employee__id=emp_id)

    context = {
        "attendance": attendance,
        "employees": employees,
        "selected_month": month,
        "selected_department": department,
        "selected_employee": emp_id,
    }

    return render(request, "hr_attendance_panel.html", context)


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
from datetime import datetime,timedelta
from django.shortcuts import render, redirect
from .models import Employees, Emp_Attendance


from datetime import datetime, timedelta
from django.db.models.functions import ExtractMonth, ExtractYear
from django.shortcuts import render, redirect
from .models import Employees, Emp_Attendance

@login_required
def employee_attendance_view(request):
    emp = Employees.objects.get(user=request.user)

    now = datetime.now()
    today_date = now.date()
    current_time = now.time().strftime("%H:%M:%S")

    # Get or create today's attendance
    attendance, created = Emp_Attendance.objects.get_or_create(
        employee=emp,
        date=today_date,
    )

    # ------------ LOGIN / LOGOUT HANDLING ------------
    if request.method == "POST":
        action = request.POST.get("action")

        # LOGIN
        if action == "login" and attendance.check_in is None:
            attendance.check_in = now.time()
            attendance.status = "present"
            attendance.save()

        # LOGOUT
        elif action == "logout" and attendance.check_in and attendance.check_out is None:
            attendance.check_out = now.time()

            # Calculate working hours
            check_in_dt = datetime.combine(today_date, attendance.check_in)
            check_out_dt = datetime.combine(today_date, now.time())
            worked_seconds = (check_out_dt - check_in_dt).total_seconds()
            attendance.total_hours =(timedelta(seconds=worked_seconds))

            attendance.save()

        return redirect("emp_dashboard")

    # ------------ SHOW HISTORY ONLY WHEN ASKED ------------
    show_history = request.GET.get("show_history")

    # Month selection
    selected_month = request.GET.get("month")
    selected_year = request.GET.get("year")

    month = int(selected_month) if selected_month else now.month
    year = int(selected_year) if selected_year else now.year

    # Attendance History Filter
    attendance_history = Emp_Attendance.objects.filter(
        employee=emp,
        date__month=month,
        date__year=year
    ).order_by('-date')

    # List of months available
    months = (
        Emp_Attendance.objects.filter(employee=emp)
        .annotate(month=ExtractMonth('date'), year=ExtractYear('date'))
        .values('month', 'year')
        .distinct()
        .order_by('-year', '-month')
    )

    return render(request, "Employee/emp_attendance.html", {
        "today": today_date,
        "current_time": current_time,
        "checkin": attendance.check_in,
        "checkout": attendance.check_out,
        "total_hours": attendance.total_hours,

        # HISTORY DATA
        "show_history": show_history,
        "attendance_history": attendance_history,
        "months": months,
        "selected_month": month,
        "selected_year": year,
    })


def id_card_view(request):
    user = request.user

    # If employee doesn't exist → emp = None
    emp = Employees.objects.filter(user=user).first()

    if not emp:
        return render(request, "Employee/id_card.html", {"id_details": None})

    id_details = Idcord.objects.filter(employee=emp)

    return render(request, "Employee/id_card.html", {"id_details": id_details})




