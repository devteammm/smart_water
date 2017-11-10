from django.shortcuts import render
from django.http import HttpResponse
from water_company import views as water_company_views
from customer import views as customer_views
from water_staff import views as water_staff_views

from .apis import calculate_at

def home(request):

    if request.user.is_authenticated():
        if request.user.is_customer:
            return customer_views.home(request)
        if request.user.is_water_company:
            return water_company_views.home(request)
        if request.user.is_water_staff:
            return water_staff_views.home(request)

    return render(request,'main/home.html',{})

def canculate(request,month=None,year=None):

    if month is None or year is None:
        return HttpResponse('Mounth and year are not valid!')

    canculate_at(int(month),int(year))

    return HttpResponse('DONE')
