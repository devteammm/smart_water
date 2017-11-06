from functools import reduce
from .models import *
from sysauth import *

def calculate_water_device_used(month,year,update=False):
    digital_devices = DigitalWaterDevice.objects.filter(active=True)
    mechanics_devices = MechanicsWaterDevice.objects.filter(active=True)

    for device in digital_devices:
        du = None
        try:
            du = DigitalWaterDeviceUsed.objects.get(month = month,year=year,device=device)
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

        du.month = month
        du.year = year
        du.device = device
        du.collect = collect
        du.collect_before = collect_before
        du.used = used
        du.save()

    for device in mechanics_devices:
        du = None
        try:
            du = MechanicsWaterDeviceUsed.objects.get(month = month,year=year,device=device)
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

        du.month = month
        du.year = year
        du.device = device
        du.collect = collect
        du.collect_before = collect_before
        du.used = used
        du.save()

def create_water_bill_for_customer(customer,month,year,update=True):
    bill = None
    try:
        bill = WaterBill.objects.get(customer = customer,month=month,year=year)
        if not update:
            return
    except WaterBill.DoesNotExist as e:
        bill = WaterBill()

    bill.year=year
    bill.month = month
    bill.customer = customer

    try:
        bill.digital_water_device_used = DigitalWaterDeviceUsed.objects.get(device__customer=customer, device__active=True,month=month,year=year)
    except DigitalWaterDeviceUsed.DoesNotExist as e:
        pass

    try:
        bill.mechanics_water_device_used = MechanicsWaterDeviceUsed.objects.get(device__customer=customer, device__active=True,month=month,year=year)
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

    bill.price = 2000
    bill.total = bill.used * bill.price
    bill.is_paid = False if bill.total > 0 else True
    bill.save()


def create_water_bill(month,year):
    customers = Customer.objects.all()
    for customer in customers:
        create_water_bill_for_customer(customer,month,year)

def calculate_at(month,year):
    calculate_water_device_used(month,year)
    create_water_bill(month,year)
