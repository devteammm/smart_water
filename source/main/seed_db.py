from .models import *
from sysauth.models import *
from random import randint

from .apis import calculate_at

def clear_db():
    WaterCompany.objects.all().delete()
    WaterDepartment.objects.all().delete()
    User.objects.filter(is_superuser = False).delete()

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
    WaterCompany.objects.create(name='company 1',address='ha noi', phone='012345678')

def create_water_company_staff():
    print('create_water_company_staff')
    user = User.objects.create_user(username='water_company_staff1',password='1',email='staff@staff.com')
    user.is_water_company_staff = True
    user.water_company_staff_profile = WaterCompanyStaff.objects.create(user=user,name='company staff 1',phone='012345678')
    user.save()

    user = User.objects.create_user(username='water_company_staff2',password='1',email='staff@staff.com')
    user.is_water_company_staff = True
    user.water_company_staff_profile = WaterCompanyStaff.objects.create(user=user,name='company staff 2', phone = '012345678')
    user.save()
    return user

def create_water_department():
    print('create_water_department')
    WaterDepartment.objects.create(name='water_department1',address='Ha Noi',phone='0123456789')
    WaterDepartment.objects.create(name='water_department2',address='Ha Noi',phone='0123456789')

def create_water_department_staff():
    print('create_water_department_staff')
    department1 = WaterDepartment.objects.get(name='water_department1')
    department2 = WaterDepartment.objects.get(name='water_department2')

    user = User.objects.create_user(username='water_department1_staff1',password='1',email='staff@staff.com')
    user.is_water_department_staff = True
    user.water_department_staff_profile = WaterDepartmentStaff.objects.create(user=user,department = department1,name='department staff 1',phone='012345678')
    user.save()

    user = User.objects.create_user(username='water_department1_staff2',password='1',email='staff@staff.com')
    user.is_water_department_staff = True
    user.water_department_staff_profile = WaterDepartmentStaff.objects.create(user=user,department = department1,name='department staff 2',phone='012345678')
    user.save()

    user = User.objects.create_user(username='water_department2_staff1',password='1',email='staff@staff.com')
    user.is_water_department_staff = True
    user.water_department_staff_profile = WaterDepartmentStaff.objects.create(user=user,department = department2,name='department staff 3',phone='012345678')
    user.save()

    user = User.objects.create_user(username='water_department2_staff2',password='1',email='staff@staff.com')
    user.is_water_department_staff = True
    user.water_department_staff_profile = WaterDepartmentStaff.objects.create(user=user,department = department2,name='department staff 4',phone='012345678')
    user.save()


def create_customer():
    print('create_customer')
    department1 = WaterDepartment.objects.get(name='water_department1')
    department2 = WaterDepartment.objects.get(name='water_department2')

    # --------------------------

    user = User.objects.create_user(username='digital_customer1',password='1',email='customer@customer.com')
    user.is_customer = True
    user.customer_profile = Customer.objects.create(water_department=department1, user=user,name='digital customer 1',address='Ha Noi',phone='012345678')
    user.save()
    device = DigitalWaterDevice.objects.create(customer = user.customer_profile,token='digital_device1',active=True)

    # --------------------------

    user = User.objects.create_user(username='mechanics_customer1',password='1',email='customer@customer.com')
    user.is_customer = True
    user.customer_profile = Customer.objects.create(water_department=department1, user=user,name='mechanics customer 2',address='Ha Noi',phone='012345678')
    user.save()
    device = MechanicsWaterDevice.objects.create(customer = user.customer_profile,token='mechanics_device1',active=True)

    # --------------------------

    user = User.objects.create_user(username='digital_customer2',password='1',email='customer@customer.com')
    user.is_customer = True
    user.customer_profile = Customer.objects.create(water_department=department2, user=user,name='digital customer 2',address='Ha Noi',phone='012345678')
    user.save()
    device = DigitalWaterDevice.objects.create(customer = user.customer_profile,token='digital_device_2',active=True)

    # --------------------------

    user = User.objects.create_user(username='mechanics_customer2',password='1',email='customer@customer.com')
    user.is_customer = True
    user.customer_profile = Customer.objects.create(water_department=department2, user=user,name='mechanics customer 2',address='Ha Noi',phone='012345678')
    user.save()
    device = MechanicsWaterDevice.objects.create(customer = user.customer_profile,token='mechanics_device_2',active=True)

SEED_TIMES = (
    (5,2017),
    (6,2017),
    (7,2017),
    (8,2017),
    (9,2017),
    (10,2017),
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
        for month,year in SEED_TIMES:
            value = randint(20,200) + last_value
            last_value = value
            DigitalWaterDeviceCollect.objects.create(year=year,month=month,device=device,value=value)

    for device in mechanics_devices:
        begin_value = device.begin_value
        last_value = begin_value
        for month,year in SEED_TIMES:
            value = randint(20,200) + last_value
            last_value = value
            MechanicsWaterDeviceCollect.objects.create(year=year,month=month,device=device,value=value)

def seed_water_price_config():

    print('seed_water_price_config')

    for month, year in SEED_TIMES:
        default_price = randint(1000,4000)
        config = WaterPriceConfig.objects.create(month = month,year=year,default_price=default_price)

        max_value = randint(20,40)
        price = randint(1000,4000)
        WaterPrice.objects.create(config=config,min_value=WaterPrice.NOT_SET,max_value=max_value,price=price)
        last_value = max_value
        last_price = price

        loop = randint(1,4)
        for i in range(loop):
            min_value = last_value +1
            max_value = randint(min_value+10, min_value + 20)
            price = randint(last_price + 500, last_price + 1000)

            WaterPrice.objects.create(config=config,min_value=min_value,max_value=max_value,price=price)

            last_value = max_value
            last_price = price

        min_value = last_value +1
        price =  randint(last_price +500,last_price+ 1000)
        WaterPrice.objects.create(config=config,min_value=min_value,max_value=WaterPrice.NOT_SET,price=price)

def seed_db():
    print('seed_db')
    create_water_company()
    create_water_company_staff()

    create_water_department()
    create_water_department_staff()

    create_customer()

    seed_device_collect()

    seed_water_price_config()

    print('calculate used and create bill')
    global SEED_TIMES
    for month,year in SEED_TIMES:
        calculate_at(month,year)
