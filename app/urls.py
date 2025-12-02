from django.urls import path
from .views import *

urlpatterns=[
    path('create/',signup_view,name='create'),
    path('login',login_view,name='login'),
    path('emp_dashboard/',dashborad_view,name='emp_dashboard'),
    path('hr_dashboard/',HR_dashborad_view,name='hr_dashboard'),
    path('employee',employee_view,name="employee"),
    path('employee_edit/<int:id>/',emlployee_edit_view,name='employee_edit'),
    path('employee_delete/<int:id>/',employee_delete_view,name='employee_delete'),

]