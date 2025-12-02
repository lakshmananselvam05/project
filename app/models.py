from django.db import models # pyright: ignore[reportMissingModuleSource]
from django.contrib.auth.models import AbstractUser  # pyright: ignore[reportMissingModuleSource]

# Create your models here.

class CustomUser(AbstractUser):
    roles = [("hr","HR"),("employee","Employee")]
    role = models.CharField(choices=roles)

class Employees(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=20)
    emp_id=models.PositiveIntegerField()
    email=models.EmailField()
    Gender=models.CharField(choices=[('Male','Male'),('Female','Female'),('other','other')])
    phone=models.IntegerField()
    depertment=models.CharField(choices=[('HR','HR'),('IT','IT'),('Finance','Finance'),('Marketing','Marketing'),('Sales','Sales')])
    designation=models.CharField()
    salary=models.IntegerField()
    photo=models.ImageField(upload_to='image',blank=True,null=True)

    def __str__(self):
        return self.name
    
