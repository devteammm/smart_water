from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request,'water_company/water_company_home.html',{})
