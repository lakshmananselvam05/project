from django.contrib import admin # pyright: ignore[reportMissingModuleSource]
from django.contrib.auth.admin import UserAdmin # pyright: ignore[reportMissingModuleSource]
from .models import CustomUser
from app.models import *
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ["username","email","role"]  

    add_fieldsets = UserAdmin.add_fieldsets+ (("Additional Info",{"fields":("role",),}),) 

    fieldsets = UserAdmin.fieldsets + (("Additional Info",{"fields":("role",),}),) 

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Employees)