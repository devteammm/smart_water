from .models import *
from sysauth.models import *
from random import randint

from .apis import calculate_at, get_or_create_time


def clear_db():
    WaterCompany.objects.all().delete()
    WaterStaff.objects.all().delete()
    Customer.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()

    DigitalWaterDevice.objects.all().delete()
    MechanicsWaterDevice.objects.all().delete()

    DigitalWaterDeviceCollect.objects.all().delete()
    MechanicsWaterDeviceCollect.objects.all().delete()

    DigitalWaterDeviceUsed.objects.all().delete()
    MechanicsWaterDeviceUsed.objects.all().delete()

    WaterPriceConfig.objects.all().delete()
    WaterPrice.objects.all().delete()

    WaterBill.objects.all().delete()


def create_water_company():
    print('create_water_company')
    WaterCompany.objects.create_water_company(
        username='hanoiwater', password='1', name='Ha Noi Water', address='Ha Noi', phone='012345678')


def create_water_staff():
    print('create_water_staff')

    company = WaterCompany.objects.get(user__username='hanoiwater')

    WaterStaff.objects.create_water_staff(company=company, username='water_staff1',
                                          password='1', name='Ha Noi Water Staff 1', address='Ha Noi', phone='012345678')
    WaterStaff.objects.create_water_staff(company=company, username='water_staff2',
                                          password='1', name='Ha Noi Water Staff 2', address='Ha Noi', phone='012345678')
    WaterStaff.objects.create_water_staff(company=company, username='water_staff3',
                                          password='1', name='Ha Noi Water Staff 3', address='Ha Noi', phone='012345678')
    WaterStaff.objects.create_water_staff(company=company, username='water_staff4',
                                          password='1', name='Ha Noi Water Staff 4', address='Ha Noi', phone='012345678')


def create_customer():
    print('create_customer')

    company = WaterCompany.objects.get(user__username='hanoiwater')
    print('company')
    print(company)

    # --------------------------
    customer = Customer.objects.create_customer(
        company=company, username='digital_customer1', password='1', name='digital customer 1', address='Ha Noi', phone='012345678')
    device = DigitalWaterDevice.objects.create(
        customer=customer, token='digital_device1', active=True)

    # --------------------------
    customer = Customer.objects.create_customer(
        company=company, username='mechanics_customer1', password='1', name='mechanics customer 1', address='Ha Noi', phone='012345678')
    device = MechanicsWaterDevice.objects.create(
        customer=customer, token='mechanics_device1', active=True)

    # --------------------------
    customer = Customer.objects.create_customer(
        company=company, username='digital_customer2', password='1', name='digital customer 2', address='Ha Noi', phone='012345678')
    device = DigitalWaterDevice.objects.create(
        customer=customer, token='digital_device_2', active=True)

    # --------------------------
    customer = Customer.objects.create_customer(
        company=company, username='mechanics_customer2', password='1', name='mechanics customer 2', address='Ha Noi', phone='012345678')
    device = MechanicsWaterDevice.objects.create(
        customer=customer, token='mechanics_device_2', active=True)


SEED_TIMES = (
    (5, 2017),
    (6, 2017),
    (7, 2017),
    (8, 2017),
    (9, 2017),
    (10, 2017),
)


def seed_device_collect():
    print('seed_device_collect')
    digital_devices = DigitalWaterDevice.objects.all()
    mechanics_devices = MechanicsWaterDevice.objects.all()

    devices = []
    devices.extend(digital_devices)
    devices.extend(mechanics_devices)

    global SEED_TIMES

    for device in digital_devices:
        begin_value = device.begin_value
        last_value = begin_value
        for month, year in SEED_TIMES:
            value = randint(20, 200) + last_value
            last_value = value
            time = get_or_create_time(month=month, year=year)
            DigitalWaterDeviceCollect.objects.create(
                time=time, device=device, value=value)

    for device in mechanics_devices:
        begin_value = device.begin_value
        last_value = begin_value
        for month, year in SEED_TIMES:
            value = randint(20, 200) + last_value
            last_value = value
            time = get_or_create_time(month=month, year=year)
            MechanicsWaterDeviceCollect.objects.create(
                time=time, device=device, value=value)


def seed_water_price_config():

    print('seed_water_price_config')

    CONFIG_SEED_TIMES = (
        (5, 2017),
        (6, 2017),
        (7, 2017),
        (8, 2017),
        (9, 2017),
        (10, 2017),
        (11, 2017),
    )

    for month, year in CONFIG_SEED_TIMES:
        default_price = randint(1000, 4000)
        time = get_or_create_time(month=month, year=year)
        config = WaterPriceConfig.objects.create(
            time=time, default_price=default_price)

        max_value = randint(20, 40)
        price = randint(1000, 4000)
        WaterPrice.objects.create(
            config=config, min_value=WaterPrice.NOT_SET, max_value=max_value, price=price)
        last_value = max_value
        last_price = price

        loop = randint(1, 4)
        for i in range(loop):
            min_value = last_value + 1
            max_value = randint(min_value + 10, min_value + 20)
            price = randint(last_price + 500, last_price + 1000)

            WaterPrice.objects.create(
                config=config, min_value=min_value, max_value=max_value, price=price)

            last_value = max_value
            last_price = price

        min_value = last_value + 1
        price = randint(last_price + 500, last_price + 1000)
        WaterPrice.objects.create(
            config=config, min_value=min_value, max_value=WaterPrice.NOT_SET, price=price)


def seed_db():
    print('seed_db')
    create_water_company()
    create_water_staff()

    create_customer()

    seed_device_collect()

    seed_water_price_config()

    print('calculate used and create bill')
    global SEED_TIMES
    for month, year in SEED_TIMES:
        calculate_at(month, year)
