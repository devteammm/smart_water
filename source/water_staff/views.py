from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count,Max,Min,Sum
import datetime
import json
from main.fusioncharts import FusionCharts

from main.models import *
from main.apis import *

def home(request):
    if not(request.user.is_authenticated() and request.user.is_water_staff):
        return HttpResponse('Chỉ dành cho nhân viên nước!')

    water_staff = request.user.water_staff_profile
    company = water_staff.company

    return render(request,'water_staff/water_staff_home.html',{
        'water_staff': water_staff,
        'company': company
    })

def customer_management(request):

    if not(request.user.is_authenticated() and request.user.is_water_staff):
        return HttpResponse('Chỉ dành cho nhân viên nước!')

    water_staff = request.user.water_staff_profile
    company = water_staff.company
    customers = company.customers.all()

    return render(request,'water_staff/customer_management.html',{
        'water_staff': water_staff,
        'company': company,
        'customers': customers
    })
def customer_management(request):

    if not(request.user.is_authenticated() and request.user.is_water_staff):
        return HttpResponse('Chỉ dành cho nhân viên nước!')

    water_staff = request.user.water_staff_profile
    company = water_staff.company
    customers = company.customers.all()

    return render(request,'water_staff/customer_management.html',{
        'water_staff': water_staff,
        'company': company,
        'customers': customers
    })

def revenue_chart(company=None,r = 12):
    times = Month.objects.all()

    top_12_time = times[:12]
    top_12_time =  top_12_time.reverse()
    month_label = [{'label': '%s / %s'%(time.month,time.year)} for time in top_12_time]

    total_money_top_12 = [{'value':
        '%s'% get_total_money(company,month=time.month,year=time.year)}
        for time in top_12_time
        ]

    paid_money_top_12 = [{'value':
        '%s'%get_total_money(company,month=time.month,year=time.year)}
        for time in top_12_time
        ]

    revenue_source = {}
    revenue_source["chart"] = {
        "caption": 'Thong ke doanh thu',
        "subcaption": '12 thang gan nhat',
        "xaxisname": "Thang",
        "yaxisname": "So tien (VND)",
        "numberprefix": "VND",
        "theme": "ocean"
    }
    revenue_source["categories"] = [{
        "category": month_label
    }]


    revenue_source["dataset"] = [{
            "seriesname": "Tong so tien can thu",
            "data": total_money_top_12
        }, {
            "seriesname": "Tong so tien thu duoc",
            "showvalues": "0",
            "data": paid_money_top_12
        }
    ]

    # Create an object for the mscombi2d chart using the FusionCharts class constructor
    chart = FusionCharts("mscombi2d", "ex3", "100%", 400, "revenue_chart", "json", revenue_source)

    return chart

def used_chart(company=None,r = 12):
    times = Month.objects.all()

    top_12_time = times[:12]
    top_12_time = top_12_time.reverse()
    month_label = [{'label': '%s / %s'%(time.month,time.year)} for time in top_12_time]

    total_used_top_12 = [{'value':
        '%s'% get_total_used(company,month=time.month,year=time.year)}
        for time in top_12_time
        ]

    revenue_source = {}
    revenue_source["chart"] = {
        "caption": 'Thong ke su dung nuoc',
        "subcaption": '12 thang gan nhat',
        "xaxisname": "Thang",
        "yaxisname": "So nuoc",
        # "numberprefix": "VND",
        "theme": "ocean"
    }
    revenue_source["categories"] = [{
        "category": month_label
    }]

    revenue_source["dataset"] = [{
            "seriesname": "Tong so nuoc da su dung",
            "data": total_used_top_12
        }
    ]

    # Create an object for the mscombi2d chart using the FusionCharts class constructor
    chart = FusionCharts("mscombi2d", "total_used_chart", "100%", 400, "used_chart", "json", revenue_source)

    return chart


def revenue_statistics(request):

    if not(request.user.is_authenticated() and request.user.is_water_staff):
        return HttpResponse('Chỉ dành cho nhân viên nước!')

    water_staff = request.user.water_staff_profile
    company = water_staff.company

    now = datetime.datetime.now()
    current_month = now.month
    current_year = now.year

    times = Month.objects.all()

    revenue_statistics_per_month = []

    for time in times:

        month = time.month
        year = time.year

        customer_count = company.customers.count()
        paid_customer_count = WaterBill.objects.filter(customer__company = company, time = time,is_paid=True).count()

        total_used = WaterBill.objects.filter(customer__company = company, time = time).aggregate(Sum('used'))['used__sum']

        total_money = WaterBill.objects.filter(customer__company = company, time = time).aggregate(Sum('total'))['total__sum']
        paid_money = WaterBill.objects.filter(customer__company = company, time = time,is_paid=True).aggregate(Sum('total'))['total__sum']
        if paid_money is None:
            paid_money = 0

        rs = {
            'month': month,
            'year': year,
            'customer_count': customer_count,
            'paid_customer_count': paid_customer_count,
            'total_used': total_used,
            'total_money': total_money,
            'paid_money': paid_money
        }

        revenue_statistics_per_month.append(rs)




    return render(request,'water_staff/revenue_statistics.html',{
        'water_staff': water_staff,
        'company': company,
        'current_month': current_month,
        'current_year': current_year,
        'revenue_statistics_per_month': revenue_statistics_per_month,
        'revenue_chart': revenue_chart(company=company).render(),
        'used_chart': used_chart(company=company).render(),
    })
