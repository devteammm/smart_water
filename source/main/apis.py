from functools import reduce
from .models import *
from sysauth import *

def calculate_water_device_used(mouth,year,update=False):
    digital_devices = DigitalWaterDevice.objects.filter(active=True)
    mechanics_devices = MechanicsWaterDevice.objects.filter(active=True)

    for device in digital_devices:
        du = None
        try:
            du = DigitalWaterDeviceUsed.objects.get(mouth = mouth,year=year,device=device)
            if not update:
                continue
        except DigitalWaterDeviceUsed.DoesNotExist as e:
            du = DigitalWaterDeviceUsed()

        collect = device.last_collect_at(mouth,year)
        collect_before = device.last_collect_before(mouth,year)

        used = None
        if collect is not None:
            if collect_before is not None:
                used = collect.value - collect_before.value
            else:
                used = collect.value - device.begin_value

        du.mouth = mouth
        du.year = year
        du.device = device
        du.collect = collect
        du.collect_before = collect_before
        du.used = used
        du.save()

    for device in mechanics_devices:
        du = None
        try:
            du = MechanicsWaterDeviceUsed.objects.get(mouth = mouth,year=year,device=device)
            if not update:
                continue
        except MechanicsWaterDeviceUsed.DoesNotExist as e:
            du = MechanicsWaterDeviceUsed()

        collect = device.last_collect_at(mouth,year)
        collect_before = device.last_collect_before(mouth,year)

        used = None
        if collect is not None:
            if collect_before is not None:
                used = collect.value - collect_before.value
            else:
                used = collect.value - device.begin_value

        du.mouth = mouth
        du.year = year
        du.device = device
        du.collect = collect
        du.collect_before = collect_before
        du.used = used
        du.save()

def create_water_bill_for_customer(customer,mouth,year,update=True):
    bill = None
    try:
        bill = WaterBill.objects.get(customer = customer,mouth=mouth,year=year)
        if not update:
            return
    except WaterBill.DoesNotExist as e:
        bill = WaterBill()

    bill.year=year
    bill.mouth = mouth
    bill.customer = customer

    try:
        bill.digital_water_device_used = DigitalWaterDeviceUsed.objects.get(device__customer=customer, device__active=True,mouth=mouth,year=year)
    except DigitalWaterDeviceUsed.DoesNotExist as e:
        pass

    try:
        bill.mechanics_water_device_used = MechanicsWaterDeviceUsed.objects.get(device__customer=customer, device__active=True,mouth=mouth,year=year)
    except MechanicsWaterDeviceUsed.DoesNotExist as e:
        pass


    if bill.digital_water_device_used is None and bill.mechanics_water_device_used is None:
        bills = WaterBill.objects.filter(customer = customer).order_by('-year','-mouth')[:3]
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

    bill.price = 10
    bill.total = bill.used * bill.price
    bill.is_paid = False if bill.total > 0 else True
    bill.save()


def create_water_bill(mouth,year):
    customers = Customer.objects.all()
    for customer in customers:
        create_water_bill_for_customer(customer,mouth,year)

def calculate_at(mouth,year):
    calculate_water_device_used(mouth,year)
    create_water_bill(mouth,year)
