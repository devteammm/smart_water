from django.db import models
from sysauth.models import Customer

MOUNTHS = (
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
    (6,6),
    (7,7),
    (8,8),
    (9,9),
    (10,10),
    (11,11),
    (12,12)
)

class DigitalWaterDevice(models.Model):
    customer = models.ForeignKey(Customer,related_name='digital_water_devices')
    token = models.CharField(default='',max_length = 255)
    active = models.BooleanField(default=False)

    def __str__(self):
        return '"%s" [digital] of user "%s"' %(self.token, self.customer)
    def __unicode__(self):
        return self.__str__()

class MechanicsWaterDevice(models.Model):
    customer = models.ForeignKey(Customer,related_name='mechanics_water_devices')
    token = models.CharField(default='',max_length = 255)
    active = models.BooleanField(default=False)

    def __str__(self):
        return '"%s" [mechanics] of user "%s"' %(self.token, self.customer)
    def __unicode__(self):
        return self.__str__()


class DigitalWaterDeviceCollect(models.Model):

    year = models.IntegerField(default=1)
    mounth = models.IntegerField(default=1,choices=MOUNTHS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    water_device = models.ForeignKey(DigitalWaterDevice,related_name='collects')
    value = models.IntegerField(default=0)

    def __str__(self):
        return 'mounth "%s", value "%s",device "%s"'% (self.mounth,self.value,self.water_device)
    def __unicode__(self):
        return self.__str__()


class MechanicsWaterDeviceCollect(models.Model):

    year = models.IntegerField(default=1)
    mounth = models.IntegerField(default=1,choices=MOUNTHS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    water_device = models.ForeignKey(MechanicsWaterDevice,related_name='collects')
    value = models.IntegerField(default=0)

    def __str__(self):
        return 'mounth "%s", value "%s",device "%s"'% (self.mounth,self.value,self.water_device)
    def __unicode__(self):
        return self.__str__()

class WaterInfo(models.Model):
    year = models.IntegerField(default=1)
    mounth = models.IntegerField(default=1,choices=MOUNTHS)

    customer = models.ForeignKey(Customer,related_name='water_infors')

    digital_water_device_collect = models.ForeignKey(DigitalWaterDeviceCollect,null=True)
    mechanics_water_device_collect = models.ForeignKey(MechanicsWaterDeviceCollect,null=True)

    value = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return '%s - %s, %s, value "%s", price "%s", total: "%s"' % (self.mounth,self.year,self.customer,self.value,self.price,self.total)
    def __unicode__(self):
        return self.__str__()
