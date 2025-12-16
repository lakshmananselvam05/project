from django.shortcuts import render,redirect,HttpResponse  # pyright: ignore[reportMissingModuleSource]
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomSignupForm,EmployeeForm
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q ,Count,Sum,Avg, Max, Min
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

    # Employee counts
    emp = Employees.objects.count()
    it = Employees.objects.filter(depertment='IT').count()
    finance = Employees.objects.filter(depertment='Finance').count()
    marketing = Employees.objects.filter(depertment='Marketing').count()
    sales = Employees.objects.filter(depertment='Sales').count()

    

    # Attendance counts
    attendance = Emp_Attendance.objects.filter(date=datetime.now().date())
   
    attendance_count = attendance.count()
   
    date = datetime.now().date()
    present_count = attendance.filter(status='present',date=date).count()

    absent_count = attendance.filter(status='absent',date=date).count()

    context = {
        'emp': emp,
        'it': it,
        'finance': finance,
        'marketing': marketing,
        'sales': sales,
        'attendance_count': attendance_count,
        'present_count': present_count,
        'absent_count': absent_count,
    }

    return render(request, 'hr_dashboard.html', context)




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


# from django.shortcuts import render
# from django.db.models import Q
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

from datetime import date
from django.shortcuts import render
from .models import Employees, Emp_Attendance




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


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Employees, Emp_Attendance

@login_required
def dashboard_view(request):
    # Get the logged-in employee
    emp = get_object_or_404(Employees, user=request.user)

    # Get all attendance records for this employee, latest first
    attendance_list = Emp_Attendance.objects.filter(employee=emp).order_by('-date')

    # Today's date
    today = datetime.now().date()

    # Count present and absent days for the current month
    present_days = attendance_list.filter(status__icontains="present", date__month=today.month, date__year=today.year).count()
    absent_days = attendance_list.filter(status__icontains="leave", date__month=today.month, date__year=today.year).count()
    print(absent_days)

    context = {
        'employee': emp,
        'attendance_list': attendance_list[:5],  # show latest 5 records
        'present_days': present_days,
        'absent_days': absent_days,
    }

    return render(request, 'Employee/employee_dashboard.html', context)


   


from datetime import datetime
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
            attendance.total_hours = round((check_out_dt - check_in_dt).total_seconds() / 3600, 2)

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


def employee_salary_view(request):
    date = datetime.now()
    month = date.strftime("%B")
    
    year = date.year
    data=emp_Salary.objects.filter(month=month,year=year)
    if request.method=="POST":
     
         month = request.POST.get("month") 
         print(month)     # format: YYYY-MM

         if month:
            m = datetime.strptime(month, "%Y-%m")
            mon= m.strftime("%B")
          
            data=emp_Salary.objects.filter(month=mon,year=m.year)
            return render(request,'salary.html',{'data':data})
    return render(request,'salary.html',{'data':data})




def generate_salary(request):
    month = request.GET.get("month")

    # 🚨 HARD STOP if month is empty or missing
    if not month:
        return redirect('emp-salary')

    # ✅ Now m is GUARANTEED
    m = datetime.strptime(month, "%Y-%m")

    employees = Employees.objects.all()

    for emp in employees:
        attendance_qs = Emp_Attendance.objects.filter(
            employee=emp,
            date__year=m.year,
            date__month=m.month
        )

        calculate_salary(emp, attendance_qs, m)

    return redirect('emp-salary')




def calculate_salary(employee, attendance_qs, month_obj):
    # Count present days
    present_days = attendance_qs.filter(status="Present").count()

    # Example: assume employee has a daily salary
    # If your Employees model has salary_per_day field, use it
    daily_salary = employee.salary/30

    # Calculate salary
    total_salary = present_days * daily_salary

    # Save to emp_Salary table
    emp_Salary.objects.update_or_create(
        employee=employee,
        month=month_obj.strftime("%B"),  # Example: "January"
        year=month_obj.year,
        defaults={
            "present_days": present_days,
            "salary": total_salary,
        }
    )

def employee_salary_slip(request,sal_id,sal_date):
   
    m = datetime.strptime(sal_date, "%Y-%m-%d")
    mon=m.strftime("%B")
    salary=emp_Salary.objects.get(employee=sal_id,month=mon,year=m.year)

    print(salary)
    return render(request,'emp_salary_slip.html',{'i':salary})

#--------------------------------------------------Employee salary------------------------------------------------------------
def silp_view(request):
    emp = Employees.objects.get(user=request.user)

    salary = emp_Salary.objects.filter(employee=emp)   # GET ALL RECORDS
    return render(request, 'Employee/employee_slip_salary.html', {'salary': salary})

