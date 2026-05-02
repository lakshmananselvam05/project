from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    roles = [("hr", "HR"), ("employee", "Employee")]
    role = models.CharField(choices=roles, max_length=20, default="employee")

class Employees(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    emp_id = models.CharField(max_length=20, unique=True, blank=True)
    Gender = models.CharField(choices=[('Male','Male'),('Female','Female'),('Other','Other')], max_length=10)
    phone = models.BigIntegerField()
    depertment = models.CharField(choices=[
        ('HR','HR'),('IT','IT'),('Finance','Finance'),
        ('Marketing','Marketing'),('Sales','Sales')
    ], max_length=20)
    designation = models.CharField(max_length=50)
    salary = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='image/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.emp_id:
            last_emp = Employees.objects.order_by('-id').first()
            last_id = int(last_emp.emp_id.replace('E', '')) if last_emp and last_emp.emp_id else 0
            self.emp_id = f"E{last_id + 1:03d}"
        super().save(*args, **kwargs)


class Idcord(models.Model):
    employee = models.OneToOneField(Employees, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=255)
    Blood_Group = models.CharField(max_length=10)
    DOB = models.CharField(max_length=20)
    Emergency_contact_No = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.employee.name} - ID Card"


class Emp_Attendance(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(choices=[
        ('present','Present'),('absent','Absent'),('leave','Leave')
    ], max_length=10, null=True, blank=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    total_hours = models.FloatField(default=0)

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"


class emp_Salary(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    present_days = models.IntegerField(default=0)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.employee.name} - {self.month} {self.year}"