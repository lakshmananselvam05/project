from django.urls import path
from .views import *

urlpatterns = [
    # ── Auth ──
    path('', employee_login, name='employee-login'),
    path('create/', signup_view, name='create'),
    path('logout/', logout_view, name='logout'),

    # ── HR ──
    path('hr_dashboard/', HR_dashborad_view, name='hr_dashboard'),

    # ── Employee CRUD ──
    path('employee/', employee_view, name='employee'),
    path('employee/<int:id>/', employee_detail_view, name='employee_detail'),
    path('employee_edit/<int:id>/', emlployee_edit_view, name='employee_edit'),
    path('employee_delete/<int:id>/', employee_delete_view, name='employee_delete'),
    path('create-employees/', emplyoee_form, name='create-employee'),

    # ── ID Card ──
    path('idcard/', idcord_view, name='idcards'),
    path('create-id/<int:emp_id>/', id_cords_detalis, name='create-id'),

    # ── Attendance ──
    path('attendance/', attendance_view, name='attendance'),
    path('hr/attendance-panel/', hr_attendance_panel, name='hr_attendance_panel'),

    # ── Salary HR ──
    path('emp-salary/', employee_salary_view, name='emp-salary'),
    path('generate-salary/', generate_salary, name='gen-sal'),
    path('emp-salary-slip/<int:sal_id>/<int:sal_year>/<str:sal_month>/',
         employee_salary_slip, name='emp-salary-slip'),

    # ── Employee Portal ──
    path('emp_dashboard/', dashboard_view, name='emp_dashboard'),
    path('emp-attendance/', employee_attendance_view, name='emp-attendance'),
    path('id_card/', id_card_view, name='id-details'),
    path('silp-view/', silp_view, name='silp_view'),
]