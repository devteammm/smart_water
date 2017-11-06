from django.shortcuts import render
from django.http import HttpResponse
from . import customer_views,company_staff_views,department_staff_views

from .apis import calculate_at

def home(request):

    if request.user.is_authenticated():
        if request.user.is_customer:
            return customer_views.home(request)
        if request.user.is_water_company_staff:
            return company_staff_views.home(request)
        if request.user.is_water_department_staff:
            return department_staff_views.home(request)

    return render(request,'main/home.html',{})

def canculate(request,mouth=None,year=None):

    if mouth is None or year is None:
        return HttpResponse('Mounth and year are not valid!')

    canculate_at(int(mouth),int(year))

    return HttpResponse('DONE')
