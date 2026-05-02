from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Employees, Idcord, Emp_Attendance, emp_Salary


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display  = ['username', 'email', 'role', 'is_active']
    list_filter   = ['role', 'is_active']
    search_fields = ['username', 'email']
    fieldsets     = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )


@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    list_display   = ['emp_id', 'name', 'depertment', 'designation', 'salary', 'phone']
    list_filter    = ['depertment', 'Gender']
    search_fields  = ['name', 'emp_id', 'designation']
    ordering       = ['-id']


@admin.register(Idcord)
class IdcordAdmin(admin.ModelAdmin):
    list_display  = ['employee', 'Blood_Group', 'DOB', 'Emergency_contact_No']
    search_fields = ['employee__name']


@admin.register(Emp_Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display  = ['employee', 'date', 'status', 'check_in', 'check_out', 'total_hours']
    list_filter   = ['status', 'date']
    search_fields = ['employee__name']
    ordering      = ['-date']
    date_hierarchy = 'date'


@admin.register(emp_Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display  = ['employee', 'month', 'year', 'present_days', 'salary']
    list_filter   = ['month', 'year']
    search_fields = ['employee__name']
    ordering      = ['-year', '-month']