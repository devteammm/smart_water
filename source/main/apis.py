from .models import *
from sysauth import *
# Create your views here.


def create_water_company():
    WaterCompany.objects.create(name='company 1',address='ha noi', phone='012345678')

def create_water_company_staff():
    user = User.objects.create_user(username='water_company_staff1',password='12345678',email='staff@staff.com')
    user.is_water_company_staff = True
    user.water_company_staff_profile = WaterCompanyStaff.objects.create(user=user,name='company staff 1',phone='012345678')
    user.save()

    user = User.objects.create_user(username='water_company_staff2',password='12345678',email='staff@staff.com')
    user.is_water_company_staff = True
    user.water_company_staff_profile = WaterCompanyStaff.objects.create(user=user,name='company staff 2', phone = '012345678')
    user.save()
    return user

def create_water_department():
    WaterDepartment.objects.create(name='water_department1',address='Ha Noi',phone='0123456789')
    WaterDepartment.objects.create(name='water_department2',address='Ha Noi',phone='0123456789')

def create_water_department_staff():
    department1 = WaterDepartment.objects.get(name='water_department1')
    department2 = WaterDepartment.objects.get(name='water_department2')

    staff1 = User.objects.create_user(username='water_department1_staff1',password='12345678',email='staff@staff.com')
    staff1.is_water_department_staff = True
    staff1.water_department_staff_profile = WaterDepartmentStaff.objects.create(user=user,department = department1,name='department staff 1',phone='012345678')
    staff1.save()

    staff2 = User.objects.create_user(username='water_department1_staff2',password='12345678',email='staff@staff.com')
    staff2.is_water_department_staff = True
    staff1.water_department_staff_profile = WaterDepartmentStaff.objects.create(user=user,department = department1,name='department staff 2',phone='012345678')
    staff2.save()

    staff3 = User.objects.create_user(username='water_department2_staff1',password='12345678',email='staff@staff.com')
    staff3.is_water_department_staff = True
    staff1.water_department_staff_profile = WaterDepartmentStaff.objects.create(user=user,department = department2,name='department staff 3',phone='012345678')
    staff3.save()

    staff4 = User.objects.create_user(username='water_department2_staff2',password='12345678',email='staff@staff.com')
    staff4.is_water_department_staff = True
    staff1.water_department_staff_profile = WaterDepartmentStaff.objects.create(user=user,department = department2,name='department staff 4',phone='012345678')
    staff4.save()


def create_customer():

    department1 = WaterDepartment.objects.get(name='department1')
    department2 = WaterDepartment.objects.get(name='department2')

    # --------------------------

    user = User.objects.create_user(username='digital_customer1',pasword='12345678',email='customer@customer.com')
    user.is_customer = True
    user.customer_profile = Customer.objects.create(water_department=department1, user=user,name='digital customer 1',address='Ha Noi',phone='012345678')
    user.save()
    device = DigitalWaterDevice.objects.create(customer = user.customer_profile,token='digital_device1',active=True)

    # --------------------------

    user = User.objects.create_user(username='mechanics_customer2',pasword='12345678',email='customer@customer.com')
    user.is_customer = True
    user.customer_profile = Customer.objects.create(water_department=department1, user=user,name='mechanics customer 2',address='Ha Noi',phone='012345678')
    user.save()
    device = DigitalWaterDevice.objects.create(customer = user.customer_profile,token='mechanics_device1',active=True)

    # --------------------------

    user = User.objects.create_user(username='digital_customer2',pasword='12345678',email='customer@customer.com')
    user.is_customer = True
    user.customer_profile = Customer.objects.create(water_department=department2, user=user,name='digital customer 2',address='Ha Noi',phone='012345678')
    user.save()
    device = DigitalWaterDevice.objects.create(customer = user.customer_profile,token='digital device 2',active=True)

    # --------------------------

    user = User.objects.create_user(username='mechanics_customer2',pasword='12345678',email='customer@customer.com')
    user.is_customer = True
    user.customer_profile = Customer.objects.create(water_department=department2, user=user,name='mechanics customer 2',address='Ha Noi',phone='012345678')
    user.save()
    device = DigitalWaterDevice.objects.create(customer = user.customer_profile,token='mechanics device 2',active=True)


def seed_db():

    create_water_company()
    create_water_company_staff()

    create_water_department()
    create_water_department_staff()

    create_customer()
