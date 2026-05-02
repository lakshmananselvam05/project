from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from datetime import datetime
from .models import *
from .forms import *


# ── Signup ──────────────────────────────────────────────────────
def signup_view(request):
    form = CustomSignupForm()
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("employee-login")
        else:
            print(form.errors)
    return render(request, "create.html", {"form": form})


# ── Login ────────────────────────────────────────────────────────
def employee_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("hr_dashboard") if user.role == "hr" else redirect("emp_dashboard")
        return render(request, "Employee/emp_login.html", {"error": "Invalid credentials"})
    return render(request, "Employee/emp_login.html")


# ── Logout ───────────────────────────────────────────────────────
def logout_view(request):
    logout(request)
    return redirect("employee-login")


# ── HR Dashboard ─────────────────────────────────────────────────
def HR_dashborad_view(request):
    today      = datetime.now().date()
    attendance = Emp_Attendance.objects.filter(date=today)
    context = {
        'emp':              Employees.objects.count(),
        'it':               Employees.objects.filter(depertment='IT').count(),
        'finance':          Employees.objects.filter(depertment='Finance').count(),
        'marketing':        Employees.objects.filter(depertment='Marketing').count(),
        'sales':            Employees.objects.filter(depertment='Sales').count(),
        'attendance_count': attendance.count(),
        'present_count':    attendance.filter(status='present').count(),
        'absent_count':     attendance.filter(status='absent').count(),
        'recent_employees': Employees.objects.order_by('-id')[:5],
        'total_salary':     Employees.objects.aggregate(Sum('salary'))['salary__sum'] or 0,
        'today':            today,
    }
    return render(request, 'hr_dashboard.html', context)


# ── Employee List ─────────────────────────────────────────────────
def employee_view(request):
    search     = request.GET.get('search', '')
    department = request.GET.get('department', '')
    emp        = Employees.objects.all()
    if search:
        emp = emp.filter(name__icontains=search)
    if department:
        emp = emp.filter(depertment=department)
    return render(request, 'employee.html', {
        'emp': emp, 'search': search, 'department': department
    })


# ── Employee Detail ───────────────────────────────────────────────
def employee_detail_view(request, id):
    emp   = get_object_or_404(Employees, id=id)
    today = datetime.now().date()
    att   = Emp_Attendance.objects.filter(
        employee=emp,
        date__month=today.month,
        date__year=today.year
    )
    return render(request, 'employee_detail.html', {
        'emp':               emp,
        'present_days':      att.filter(status__icontains='present').count(),
        'absent_days':       att.filter(status__icontains='absent').count(),
        'leave_days':        att.filter(status__icontains='leave').count(),
        'latest_salary':     emp_Salary.objects.filter(employee=emp).order_by('-year', '-month').first(),
        'recent_attendance': Emp_Attendance.objects.filter(employee=emp).order_by('-date')[:10],
    })


# ── Employee Create ───────────────────────────────────────────────
def emplyoee_form(request):
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee')
    return render(request, 'create_employee_form.html', {'form': form})


# ── Employee Edit ─────────────────────────────────────────────────
def emlployee_edit_view(request, id):
    emp  = get_object_or_404(Employees, id=id)
    form = EmployeeForm(instance=emp)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=emp)
        if form.is_valid():
            form.save()
            return redirect('employee')
    return render(request, 'employee_edit.html', {'form': form})


# ── Employee Delete ───────────────────────────────────────────────
def employee_delete_view(request, id):
    get_object_or_404(Employees, id=id).delete()
    return redirect('employee')


# ── ID Card List ──────────────────────────────────────────────────
def idcord_view(request):
    return render(request, 'idcard.html', {
        'idcards': Idcord.objects.all()
    })


# ── ID Card Create/Edit ───────────────────────────────────────────
def id_cords_detalis(request, emp_id):
    emp       = get_object_or_404(Employees, id=emp_id)
    idcard, _ = Idcord.objects.get_or_create(employee=emp)
    form      = idcordform(instance=idcard)
    if request.method == 'POST':
        form = idcordform(request.POST, instance=idcard)
        if form.is_valid():
            form.save()
            return redirect('idcards')
    return render(request, "id_card.html", {"form": form, "emp": emp})


# ── Attendance List ───────────────────────────────────────────────
def attendance_view(request):
    return render(request, 'attendance.html', {
        'att': Emp_Attendance.objects.all().order_by('-date')
    })


# ── HR Attendance Panel ───────────────────────────────────────────
def hr_attendance_panel(request):
    employees  = Employees.objects.all()
    month      = request.GET.get("month")
    department = request.GET.get("department")
    emp_id     = request.GET.get("employee")
    attendance = Emp_Attendance.objects.all().order_by("-date")

    if month:
        year, mon  = month.split("-")
        attendance = attendance.filter(date__year=year, date__month=mon)
    if department:
        attendance = attendance.filter(employee__depertment=department)
    if emp_id:
        attendance = attendance.filter(employee__id=emp_id)

    return render(request, "hr_attendance_panel.html", {
        "attendance":          attendance,
        "employees":           employees,
        "selected_month":      month,
        "selected_department": department,
        "selected_employee":   emp_id,
        "present_count":       attendance.filter(status__icontains='present').count(),
        "absent_count":        attendance.filter(status__icontains='absent').count(),
        "leave_count":         attendance.filter(status__icontains='leave').count(),
    })


# ── Employee Dashboard ────────────────────────────────────────────
@login_required
def dashboard_view(request):
    emp = Employees.objects.filter(user=request.user).first()
    if not emp:
        return render(request, 'Employee/employee_dashboard.html', {
            'employee':        None,
            'attendance_list': [],
            'present_days':    0,
            'absent_days':     0,
            'latest_salary':   None,
        })
    today = datetime.now().date()
    att   = Emp_Attendance.objects.filter(employee=emp)
    return render(request, 'Employee/employee_dashboard.html', {
        'employee':        emp,
        'attendance_list': att.order_by('-date')[:5],
        'present_days':    att.filter(
            status__icontains="present",
            date__month=today.month,
            date__year=today.year
        ).count(),
        'absent_days':     att.filter(
            status__icontains="leave",
            date__month=today.month,
            date__year=today.year
        ).count(),
        'latest_salary':   emp_Salary.objects.filter(employee=emp).order_by('-year', '-month').first(),
    })


# ── Employee Attendance ───────────────────────────────────────────
@login_required
def employee_attendance_view(request):
    emp = Employees.objects.filter(user=request.user).first()
    if not emp:
        return render(request, "Employee/emp_attendance.html", {
            "employee_missing": True,
            "today":            datetime.now().date(),
            "current_time":     datetime.now().time().strftime("%H:%M:%S"),
            "checkin":          None,
            "checkout":         None,
            "total_hours":      0,
            "show_history":     None,
            "attendance_history": [],
            "months":           [],
            "selected_month":   None,
            "selected_year":    None,
        })

    now        = datetime.now()
    today_date = now.date()
    attendance, _ = Emp_Attendance.objects.get_or_create(
        employee=emp, date=today_date
    )

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "login" and not attendance.check_in:
            attendance.check_in = now.time()
            attendance.status   = "present"
            attendance.save()
        elif action == "logout" and attendance.check_in and not attendance.check_out:
            attendance.check_out = now.time()
            from datetime import datetime as dt
            check_in_dt = dt.combine(today_date, attendance.check_in)
            attendance.total_hours = round(
                (dt.combine(today_date, now.time()) - check_in_dt).total_seconds() / 3600, 2
            )
            attendance.save()
        return redirect("emp_dashboard")

    selected_month = request.GET.get("month")
    selected_year  = request.GET.get("year")
    month = int(selected_month) if selected_month else now.month
    year  = int(selected_year)  if selected_year  else now.year

    return render(request, "Employee/emp_attendance.html", {
        "employee_missing":   False,
        "today":              today_date,
        "current_time":       now.time().strftime("%H:%M:%S"),
        "checkin":            attendance.check_in,
        "checkout":           attendance.check_out,
        "total_hours":        attendance.total_hours,
        "show_history":       request.GET.get("show_history"),
        "attendance_history": Emp_Attendance.objects.filter(
            employee=emp, date__month=month, date__year=year
        ).order_by('-date'),
        "months": Emp_Attendance.objects.filter(employee=emp)
            .annotate(month=ExtractMonth('date'), year=ExtractYear('date'))
            .values('month', 'year')
            .distinct()
            .order_by('-year', '-month'),
        "selected_month": month,
        "selected_year":  year,
    })


# ── ID Card Employee ──────────────────────────────────────────────
@login_required
def id_card_view(request):
    emp = Employees.objects.filter(user=request.user).first()
    if not emp:
        return render(request, "Employee/id_card.html", {
            "id_details":      None,
            "employee_missing": True,
        })
    return render(request, "Employee/id_card.html", {
        "id_details":      Idcord.objects.filter(employee=emp),
        "employee_missing": False,
    })


# ── Salary List HR ────────────────────────────────────────────────
def employee_salary_view(request):
    now   = datetime.now()
    month = now.strftime("%B")
    year  = now.year
    data  = emp_Salary.objects.filter(month=month, year=year)

    if request.method == "POST":
        month_input = request.POST.get("month")
        if month_input:
            m   = datetime.strptime(month_input, "%Y-%m")
            mon = m.strftime("%B")
            data = emp_Salary.objects.filter(month=mon, year=m.year)
            return render(request, 'salary.html', {
                'data':           data,
                'selected_month': month_input,
            })

    return render(request, 'salary.html', {
        'data':           data,
        'selected_month': f"{year}-{now.month:02d}",
    })


# ── Generate Salary ───────────────────────────────────────────────
def generate_salary(request):
    month = request.GET.get("month")
    if not month:
        return redirect('emp-salary')
    m = datetime.strptime(month, "%Y-%m")
    for emp in Employees.objects.all():
        att = Emp_Attendance.objects.filter(
            employee=emp,
            date__year=m.year,
            date__month=m.month
        )
        present_days = att.filter(status__icontains="present").count()
        total_salary = present_days * (emp.salary / 30)
        emp_Salary.objects.update_or_create(
            employee=emp,
            month=m.strftime("%B"),
            year=m.year,
            defaults={
                'present_days': present_days,
                'salary':       round(total_salary, 2),
            }
        )
    return redirect('emp-salary')


# ── Salary Slip HR ────────────────────────────────────────────────
def employee_salary_slip(request, sal_id, sal_year, sal_month):
    salary = get_object_or_404(
        emp_Salary,
        employee__id=sal_id,
        month=sal_month,
        year=sal_year,
    )
    return render(request, 'emp_salary_slip.html', {'i': salary})


# ── Salary Slip Employee ──────────────────────────────────────────
@login_required
def silp_view(request):
    emp = Employees.objects.filter(user=request.user).first()
    if not emp:
        return render(request, 'Employee/employee_slip_salary.html', {
            "salary":           [],
            "employee_missing": True,
        })
    return render(request, 'Employee/employee_slip_salary.html', {
        'salary':           emp_Salary.objects.filter(employee=emp).order_by('-year', '-month'),
        "employee_missing": False,
    })