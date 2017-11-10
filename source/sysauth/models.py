from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from django.db.models.signals import post_save

class CustomUserManger(UserManager):

    def create_for_customer(self,company=None, username=None,password = None,name=None,address=None,phone = None):
        user = self.create_user(username=username,password=password,is_customer=True)
        customer = Customer.objects.create(company=company, user=user,name=name,address=address,phone=phone)
        user.refresh_from_db()
        return user

    def create_for_water_company(self,username=None,password = None,name=None,address=None,phone = None):
        user = self.create_user(username=username,password=password,is_water_company=True)
        customer = WaterCompany.objects.create(user=user,name=name,address=address,phone=phone)
        user.refresh_from_db()
        return user

    def create_for_water_staff(self,company=None, username=None,password = None,name=None,address=None,phone = None):
        user = self.create_user(username=username,password=password,is_water_staff=True)
        customer = WaterStaff.objects.create(company=company, user=user,name=name,address=address,phone=phone)
        user.refresh_from_db()
        return user


class User(AbstractUser):

    objects = CustomUserManger()

    is_customer = models.BooleanField(default=False,blank=True)
    is_water_company = models.BooleanField(default=False,blank=True)
    is_water_staff = models.BooleanField(default=False,blank=True)

    def __str__(self):
        return self.username
    def __unicode__(self):
        return self.__str__()

def create_profile(sender,instance,**kwargs):
    # if instance.is_customer:
    #     if not hasattr(instance,'customer_profile') or not instance.customer_profile:
    #         Customer.objects.create(user=instance,nmae='customer',address='ha noi',phone='012345678')
    #
    # if instance.is_water_company_staff:
    #     if not hasattr(instance,'water_company_staff_profile') or not instance.water_company_staff_profile:
    #         WaterCompanyStaff.objects.create(user=instance,name='water company staff',phone='012345678')
    #
    # if instance.is_water_department_staff:
    #     if not hasattr(instance,'water_department_staff_profile') or not instance.water_department_staff_profile:
    #         WaterDepartmentStaff.objects.create(user=instance,name='water deparment staff',phone='012345678')

    pass

post_save.connect(create_profile,sender=User)

class CustomerManager(models.Manager):

    def create_customer(self,*args,**kwargs):
        user = User.objects.create_for_customer(*args,**kwargs)
        return user.customer_profile

class Customer(models.Model):

    objects = CustomerManager()

    user = models.OneToOneField(User,null=False,related_name='customer_profile')

    company = models.ForeignKey('WaterCompany',related_name='customers')
    name = models.CharField(max_length=255)
    address = models.TextField(blank=False)
    phone = models.CharField(default='',max_length=31,blank=False)

    def __str__(self):
        return self.user.username
    def __unicode__(self):
        return self.__str__()

class WaterCompanyManager(models.Manager):
    def create_water_company(self,*args,**kwargs):
        user = User.objects.create_for_water_company(*args,**kwargs)
        return user.water_company_profile

class WaterCompany(models.Model):

    objects = WaterCompanyManager()

    user = models.OneToOneField(User,null=False,related_name='water_company_profile')
    name = models.CharField(max_length=255,blank=False)
    address = models.TextField(default='',blank=False)
    phone = models.CharField(default='',max_length=31)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()


class WaterStaffManager(models.Manager):
    def create_water_staff(self,*args,**kwargs):
        user = User.objects.create_for_water_staff(*args,**kwargs)
        return user.water_staff_profile

class WaterStaff(models.Model):

    objects = WaterStaffManager()

    user = models.OneToOneField(User,null=False,related_name='water_staff_profile')
    company = models.ForeignKey(WaterCompany,related_name='staffs')

    name = models.CharField(max_length=255)
    address = models.TextField(default='',blank=False)
    phone = models.CharField(default='',max_length=31)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()
