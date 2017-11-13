from functools import reduce
from .models import *
from sysauth import *
from django.db.models import Count,Max,Min,Sum

def get_customer_used(customer,month=None,year=None):
    try:
        return WaterBill.objects.get(customer=customer,time__month=month,time__year=year).used
    except WaterBill.DoesNotExist as e:
        return 0

def get_customer_money(customer,month=None,year=None):
    try:
        return WaterBill.objects.get(customer=customer,time__month=month,time__year=year).total
    except WaterBill.DoesNotExist as e:
        return 0


def get_total_used(company,month=None,year=None):
    total_used = WaterBill.objects.filter(customer__company = company, time__month = month,time__year=year).aggregate(Sum('used'))['used__sum']

    return total_used

def get_total_money(company,month=None,year=None):
    total_money = WaterBill.objects.filter(customer__company = company, time__month = month,time__year=year).aggregate(Sum('total'))['total__sum']
    return total_money

def get_paid_money(company,month=None,year=None):
    paid_money = WaterBill.objects.filter(customer__company = company, time__month = month,time__year=year,is_paid=True).aggregate(Sum('total'))['total__sum']
    return paid_money

def get_paid_customer_count(company,month=None,year=None):
    paid_customer_count = WaterBill.objects.filter(customer__company = company, time__month = month,time__year=year,is_paid=True).count()
    return paid_customer_count

def get_or_create_time(month,year):
    try:
        time = Month.objects.get(month=month,year=year)
        return time
    except Month.DoesNotExist as e:
        return Month.objects.create(month=month,year=year)

def calculate_water_device_used(month,year,update=False):
    digital_devices = DigitalWaterDevice.objects.filter(active=True)
    mechanics_devices = MechanicsWaterDevice.objects.filter(active=True)

    for device in digital_devices:
        du = None
        try:
            du = DigitalWaterDeviceUsed.objects.get(time__month = month,time__year=year,device=device)
            if not update:
                continue
        except DigitalWaterDeviceUsed.DoesNotExist as e:
            du = DigitalWaterDeviceUsed()

        collect = device.last_collect_at(month,year)
        collect_before = device.last_collect_before(month,year)

        used = None
        if collect is not None:
            if collect_before is not None:
                used = collect.value - collect_before.value
            else:
                used = collect.value - device.begin_value

        du.time = get_or_create_time(month=month,year=year)
        du.device = device
        du.collect = collect
        du.collect_before = collect_before
        du.used = used
        du.save()

    for device in mechanics_devices:
        du = None
        try:
            du = MechanicsWaterDeviceUsed.objects.get(time__month = month,time__year=year,device=device)
            if not update:
                continue
        except MechanicsWaterDeviceUsed.DoesNotExist as e:
            du = MechanicsWaterDeviceUsed()

        collect = device.last_collect_at(month,year)
        collect_before = device.last_collect_before(month,year)

        used = None
        if collect is not None:
            if collect_before is not None:
                used = collect.value - collect_before.value
            else:
                used = collect.value - device.begin_value

        du.time = get_or_create_time(month=month,year=year)
        du.device = device
        du.collect = collect
        du.collect_before = collect_before
        du.used = used
        du.save()

def create_water_bill_for_customer(customer,month,year,update=True):

    price_config = WaterPriceConfig.objects.get(time__month=month,time__year=year)

    bill = None
    try:
        bill = WaterBill.objects.get(customer = customer,time__month=month,time__year=year)
        if not update:
            return
    except WaterBill.DoesNotExist as e:
        bill = WaterBill()

    bill.time = get_or_create_time(month=month,year=year)
    bill.customer = customer

    try:
        bill.digital_water_device_used = DigitalWaterDeviceUsed.objects.get(device__customer=customer, device__active=True,time__month=month,time__year=year)
    except DigitalWaterDeviceUsed.DoesNotExist as e:
        pass

    try:
        bill.mechanics_water_device_used = MechanicsWaterDeviceUsed.objects.get(device__customer=customer, device__active=True,time__month=month,time__year=year)
    except MechanicsWaterDeviceUsed.DoesNotExist as e:
        pass


    if bill.digital_water_device_used is None and bill.mechanics_water_device_used is None:
        bills = WaterBill.objects.filter(customer = customer).order_by('-year','-month')[:3]
        s = reduce(lambda b,s: s + b.used,  bills,0)
        used = s / len(bills) if len(bills) > 0 else 0
        bill.used = used

    else:
        used = 0
        ddu = bill.digital_water_device_used
        mdu = bill.mechanics_water_device_used

        used += ddu.used if ddu is not None else 0
        used += mdu.used if mdu is not None else 0

        bill.used = used

    bill.price_config = price_config
    bill.total = price_config.total(bill.used)
    bill.is_paid = False if bill.total > 0 else True
    bill.save()


def create_water_bill(month,year):
    customers = Customer.objects.all()
    for customer in customers:
        create_water_bill_for_customer(customer,month,year)

def calculate_at(month,year):
    calculate_water_device_used(month,year)
    create_water_bill(month,year)
