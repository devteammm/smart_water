from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from functools import reduce
import json
from main.models import IssueMessage, AppRate
from django.db.models import Avg
from main.models import WaterContract, WaterBill, WaterPriceConfig, DigitalWaterDevice, MechanicsWaterDevice, DigitalWaterDeviceCollect, MechanicsWaterDeviceCollect
from random import randint
import datetime

from PIL import Image
import pytesseract

from main.apis import get_or_create_time
from .charts import customer_used_chart, customer_money_chart


def home(request):
    if not request.user.is_authenticated() or not request.user.is_customer:
        return HttpResponse('Chi danh cho Customer')

    customer = request.user.customer_profile

    water_bills = customer.water_bills.all()
    owe_bills = customer.water_bills.filter(is_paid=False)
    debt = reduce(lambda s, b: s + b.total, list(owe_bills), 0)

    now = datetime.datetime.now()
    current_month = now.month
    current_year = now.year

    current_water_contract = WaterContract.objects.contract_for_customer_at(
        customer=customer, month=current_month, year=current_year)

    current_used = 0

    digital_device = current_water_contract.digital_device

    mechanics_device = current_water_contract.mechanics_device

    digital_used = digital_device.used_at(
        current_month, current_year) if digital_device else 0
    mechanics_used = mechanics_device.used_at(
        current_month, current_year) if mechanics_device else 0

    current_used += digital_used if digital_used is not None else 0
    current_used += mechanics_used if mechanics_used is not None else 0


    current_water_price_config = WaterPriceConfig.objects.get(contract_type=current_water_contract.type,
                                                              time__month=current_month, time__year=current_year)

    return render(request, 'customer/customer_home.html', {
        'water_bills': water_bills,
        'owe_bills': owe_bills,
        'debt': debt,
        'current_year': current_year,
        'current_month': current_month,
        'digital_device': digital_device,
        'mechanics_device': mechanics_device,
        'current_used': current_used,
        'current_water_contract': current_water_contract,
        'current_water_price_config': current_water_price_config
    })


def used_statistics(request):
    if not request.user.is_authenticated() or not request.user.is_customer:
        return HttpResponse('Chi danh cho Customer')
    customer = request.user.customer_profile
    used_chart = customer_used_chart(customer=customer)
    money_chart = customer_money_chart(customer=customer)
    water_bills = WaterBill.objects.filter(customer=customer)
    return render(request, 'customer/used_statistics.html', {
        'customer': customer,
        'used_chart': used_chart.render(),
        'money_chart': money_chart.render(),
        'water_bills': water_bills
    })

def contract_info(request):
    if not request.user.is_authenticated() or not request.user.is_customer:
        return HttpResponse('Chi danh cho Customer')
    customer = request.user.customer_profile

    contracts = customer.water_contracts.all()

    return render(request,'customer/contract_info.html',{
        'customer': customer,
        'contracts': contracts
    })

def device_management(request):
    if not request.user.is_authenticated() or not request.user.is_customer:
        return HttpResponse('Chi danh cho Customer')
    customer = request.user.customer_profile

    digital_devices = DigitalWaterDevice.objects.filter(contracts__customer = customer)
    mechanics_devices = MechanicsWaterDevice.objects.filter(contracts__customer = customer)

    return render(request, 'customer/device_management.html', {
        'digital_devices': digital_devices,
        'mechanics_devices': mechanics_devices
    })


def device_info(request, device_type=None, device_token=None):
    if not request.user.is_authenticated() or not request.user.is_customer:
        return HttpResponse('Chi danh cho Customer')

    device = None

    print(device_type)
    print(device_token)
    if device_type == 'digital':
        device = get_object_or_404(DigitalWaterDevice, token=device_token)
    elif device_type == 'mechanics':
        device = get_object_or_404(MechanicsWaterDevice, token=device_token)

    collects = None

    if device is not None:
        collects = device.collects.all().order_by(
            '-time__year', '-time__month', '-created_at')

    return render(request, 'customer/device_info.html', {
        'device_type': device_type,
        'device': device,
        'collects': collects
    })


def update_mechanics_device_value(request, device_token):

    next = request.GET.get('next', request.get_full_path())

    if not request.user.is_authenticated() or not request.user.is_customer:
        return HttpResponse('Chi danh cho Customer')
    customer = request.user.customer_profile

    device = get_object_or_404(
        MechanicsWaterDevice, contracts__customer=customer, token=device_token)

    if request.method == 'POST':
        image = request.FILES.get('image')
        value = request.POST.get('value')
        print(image)
        print(value)
        if image is not None and value is not None:
            now = datetime.datetime.now()
            month = now.month
            year = now.year
            time = get_or_create_time(month=month, year=year)
            MechanicsWaterDeviceCollect.objects.create(
                time=time, device=device, image=image, value=value)
            return redirect(next)
        else:
            return render(request, 'customer/update_mechanics_device_value.html', {
                'device': device
            })
    return render(request, 'customer/update_mechanics_device_value.html', {
        'device': device
    })


@csrf_exempt
def api_update_digital_device_value(request, device_token, value):

    device = get_object_or_404(
        DigitalWaterDevice, token=device_token)

    if value is not None:
        now = datetime.datetime.now()
        month = now.month
        year = now.year
        time = get_or_create_time(month=month, year=year)
        DigitalWaterDeviceCollect.objects.create(
            time=time, device=device, value=value)
        return HttpResponse({'status': 'ok'}, status=201)
    else:
        return HttpResponse({'error': 'Need value!'}, status=404)


@csrf_exempt
def api_parse_image_device_value(request):

    image = request.FILES.get('image')
    # value = randint(20, 200)
    value = None
    try:
        value = pytesseract.image_to_string(Image.open(image))
        value = int(value)
        res = {
            'value': value
        }
        return HttpResponse(json.dumps(res), content_type='application/json')

    except Exception as e:
        res = {
            'value': value,
            'error': str(e)
        }
        return HttpResponse(json.dumps(res), content_type='application/json', status=404)


def price_info(request):

    price_configs = WaterPriceConfig.objects.all()

    return render(request, 'customer/price_info.html', {
        'price_configs': price_configs
    })


def issue_message(request):
    if not request.user.is_authenticated() or not request.user.is_customer:
        return HttpResponse('Chi danh cho Customer')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        IssueMessage.objects.create(
            customer=request.user.customer_profile, title=title, content=content)

        return render(request, 'customer/issue_message.html', {
            'messages': request.user.customer_profile.issue_messages.all()
        })
    else:
        return render(request, 'customer/issue_message.html', {
            'messages': request.user.customer_profile.issue_messages.all()
        })


def contact(request):
    return render(request, 'customer/contact.html', {})


def rate(request):
    if not request.user.is_authenticated() or not request.user.is_customer:
        return HttpResponse('Chi danh cho Customer')

    my_rate = None
    if hasattr(request.user.customer_profile, 'app_rate'):
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

    return render(request, 'customer/rate.html', {
        'my_rate': my_rate,
        'avg_rate': avg_rate,
        'app_rates': app_rates
    })
