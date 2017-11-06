from django.shortcuts import render
from django.http import HttpResponse
from company_staff import views as company_staff_views
from customer import views as customer_views
from department_staff import views as department_staff

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

def canculate(request,month=None,year=None):

    if month is None or year is None:
        return HttpResponse('Mounth and year are not valid!')

    canculate_at(int(month),int(year))

    return HttpResponse('DONE')
