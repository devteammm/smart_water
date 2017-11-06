from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from functools import reduce

from main.models import IssueMessage, AppRate
from django.db.models import Avg


def home(request):

    water_bills = request.user.customer_profile.water_bills.all()
    owe_bills = request.user.customer_profile.water_bills.filter(is_paid = False)
    debt = reduce(lambda s,b: s + b.total,list(owe_bills),0)

    return render(request,'customer/customer_home.html',{
        'water_bills': water_bills,
        'owe_bills': owe_bills,
        'debt': debt
    })

def issue_message(request):
    if not request.user.is_authenticated() or not request.user.is_customer:
        return HttpResponse('Chi danh cho Customer')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        IssueMessage.objects.create(customer = request.user.customer_profile, title=title,content=content)

        return render(request,'customer/issue_message.html',{
            'messages': request.user.customer_profile.issue_messages.all()
        })
    else:
        return render(request,'customer/issue_message.html',{
            'messages': request.user.customer_profile.issue_messages.all()
        })


def contact(request):
    return render(request,'customer/contact.html',{})

def rate(request):
    if not request.user.is_authenticated() or not request.user.is_customer:
        return HttpResponse('Chi danh cho Customer')

    my_rate = None
    if hasattr(request.user.customer_profile,'app_rate'):
        my_rate = request.user.customer_profile.app_rate

    if request.method == 'POST':
        rate = int(request.POST.get('rate'))
        message = request.POST.get('message')

        if my_rate is None:
            my_rate = AppRate()
            my_rate.customer = request.user.customer_profile

        my_rate.rate = rate
        my_rate.message = message
        my_rate.save()

    app_rates = AppRate.objects.all()

    avg_rate = AppRate.objects.all().aggregate(Avg('rate'))['rate__avg']


    return render(request,'customer/rate.html',{
        'my_rate': my_rate,
        'avg_rate': avg_rate,
        'app_rates': app_rates
    })
