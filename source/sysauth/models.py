from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class User(AbstractUser):
    is_customer = models.BooleanField(default=False,blank=True)
    is_water_company_staff = models.BooleanField(default=False,blank=True)
    is_water_department_staff = models.BooleanField(default=False,blank=True)

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

class Customer(models.Model):

    user = models.OneToOneField(User,null=False,related_name='customer_profile')
    name = models.CharField(max_length=255)
    address = models.TextField(blank=False)
    phone = models.CharField(default='',max_length=31,blank=False)

    water_department = models.ForeignKey('WaterDepartment',related_name='customers')

    def __str__(self):
        return self.user.username
    def __unicode__(self):
        return self.__str__()

class WaterCompany(models.Model):
    name = models.CharField(max_length=255,blank=False)
    address = models.TextField(default='',blank=False)
    phone = models.CharField(default='',max_length=31)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()

class WaterCompanyStaff(models.Model):
    user = models.OneToOneField(User,null=False,related_name='water_company_staff_profile')
    name = models.CharField(max_length=255)
    phone = models.CharField(default='',max_length=31)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()

class WaterDepartment(models.Model):
    name = models.CharField(max_length=255,blank=False)
    address = models.TextField(default='',blank=False)
    phone = models.CharField(default='',max_length=31)

    def __str__(self):
        return '"%s" in "%s"' % (self.name,self.company.name)

    def __unicode__(self):
        return self.__str__()


class WaterDepartmentStaff(models.Model):
    user = models.OneToOneField(User,null=False,related_name='water_department_staff_profile')
    department = models.ForeignKey(WaterDepartment,related_name='staffs')
    name = models.CharField(max_length=255)
    phone = models.CharField(default='',max_length=31)

    def __str__(self):
        return '"%s" in "%s"'%( self.user.username , self.deparment.name )

    def __unicode__(self):
        return self.__str__()
