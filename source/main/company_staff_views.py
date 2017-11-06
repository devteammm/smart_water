from django.shortcuts import render

def home(request):
    return render(request,'main/company_staff/company_staff_home.html',{})
