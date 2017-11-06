from django.shortcuts import render

def home(request):
    return render(request,'main/department_staff/department_staff_home.html',{})
