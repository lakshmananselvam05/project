from django.db import models # pyright: ignore[reportMissingModuleSource]
from django.contrib.auth.models import AbstractUser  # pyright: ignore[reportMissingModuleSource]

# Create your models here.

class CustomUser(AbstractUser):
    roles = [("hr","HR"),("employee","Employee")]
    role = models.CharField(choices=roles)

class Employees(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20)
    emp_id = models.CharField(max_length=20, unique=True, blank=True)
   
    Gender = models.CharField(choices=[('Male','Male'),('Female','Female'),('other','other')])
    phone = models.IntegerField()
    depertment = models.CharField(choices=[('HR','HR'),('IT','IT'),('Finance','Finance'),('Marketing','Marketing'),('Sales','Sales')])
    designation = models.CharField(max_length=50)
    salary = models.IntegerField()
    photo = models.ImageField(upload_to='image', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        # Auto-generate EMP ID only when creating new employee
        if not self.emp_id:
            last_emp = Employees.objects.order_by('-id').first()
            if last_emp and last_emp.emp_id:
                last_id = int(last_emp.emp_id.replace('E', ''))
            else:
                last_id = 0

            new_id = last_id + 1
            self.emp_id = f"E{new_id:03d}"     # EMP001, EMP002, EMP010 etc.

        super().save(*args, **kwargs)

    
    
class Idcord(models.Model):
    employee=models.OneToOneField(Employees,on_delete=models.CASCADE,null=True,blank=True)
    address=models.CharField()
    Blood_Group=models.CharField()
    DOB=models.CharField()
    Emergency_contact_No=models.CharField()
  

    def __str__(self):
        return self.address
    


class Emp_Attendance(models.Model):
    employee=models.ForeignKey(Employees,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.CharField(choices=[ ('Present','Present'),('Absent','Absent'),('Leave','Leave'),],null=True,blank=True)
    check_in=models.TimeField(null=True,blank=True)
    check_out=models.TimeField(null=True,blank=True)
    total_hours=models.FloatField(default=0)

    def __str__(self):
        return f"{self.employee.name} - {self.status}"   
    
class emp_Salary(models.Model):
    employee=models.ForeignKey(Employees,on_delete=models.CASCADE)
    month=models.CharField()
    year=models.IntegerField()
    present_days=models.IntegerField()
    salary=models.FloatField()
    
    def __str__(self):
        return f"{self.employee.name} {self.month}"

    
