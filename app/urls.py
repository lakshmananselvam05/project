from django.urls import path
from .views import *

urlpatterns=[
    path('create/',signup_view,name='create'),
   
    path('hr_dashboard/',HR_dashborad_view,name='hr_dashboard'),
    path('employee/',employee_view,name="employee"),
    path('employee_edit/<int:id>/',emlployee_edit_view,name='employee_edit'),
    path('employee_delete/<int:id>/',employee_delete_view,name='employee_delete'),
    path("create-employees/",emplyoee_form,name="create-employee"),
    path('idcard/',idcord_view,name="idcards"),
    path('create-id/<int:emp_id>/',id_cords_detalis,name='create-id'),

    path("login/",employee_login,name="employee-login"),
    path('attendance/',attendance_view,name='attendance'),
#-----------------------------employee details---------------------------------------------------------------------------------
    path('emp_dashboard/',dashborad_view,name='emp_dashboard'),
    path("id_card/",id_card_view,name="id-details"),
    path("emp-attendance/",employee_attendance_view,name="emp-attendance")


]