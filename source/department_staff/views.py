from django.shortcuts import render

def home(request):
    return render(request,'department_staff/department_staff_home.html',{})
