from django.db import models
from sysauth.models import Customer
import datetime
from django.db.models import Count,Max,Min,Sum, Q

MONTHS = (
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


class Month(models.Model):
    year = models.IntegerField(default=1)
    month = models.IntegerField(default=1,choices=MONTHS)

    class Meta:
        ordering = ('-year','-month')

    def __str__(self):
        return '%s / %s' %( self.month,self.year)
    def __unicode__(self):
        return self.__str__()

class WaterDeviceMixin:
    def last_collect_before(self,month,year):
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
        c = self.last_collect_at(month,year)
        return c if c is not None else self.last_collect_at(month,year)

    def last_collect_at(self,month,year):
        if year <= self.begin_year and month < self.begin_month:
            return None
        cs = self.collects.filter(time__month=month,time__year=year).order_by('-created_at')
        return cs[0] if cs.count() > 0 else None


    def value_at(self,month,year):
        if year <= self.begin_year and month < self.begin_month:
            return self.begin_value
        lc = self.last_collect_at(month,year)
        return lc.value if lc is not None else None

    def value_at_previous_month(self):
        now = datetime.datetime.now()
        previous_month = now.month
        previous_year = now.year

        if previous_month == 1:
            previous_month = 12
            previous_year -= 1
        else:
            previous_month -=1

        return self.value_at(previous_month,previous_year)


    def last_value(self):
        last_collect = self.collects.order_by('-created_at')
        return last_collect[0].value if len(last_collect) > 0 else self.begin_value

    def last_value_before(self,month,year):
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
        value = self.value_at(month,year)
        return value if value is not None else self.last_value_before(month,year)

    def used_at(self,month,year):
        value = self.value_at(month,year)
        last_value_before = self.last_value_before(month,year)
        return value - last_value_before if value is not None and last_value_before is not None else None

    def used_at_current_month(self):
        now = datetime.datetime.now()
        return self.used_at(now.month,now.year)

class DigitalWaterDevice(models.Model,WaterDeviceMixin):
    # customer = models.ForeignKey(Customer,related_name='digital_water_devices')
    token = models.CharField(default='',max_length = 255)
    active = models.BooleanField(default=False)

    begin_value = models.IntegerField(default=0)

    begin_month = models.IntegerField(choices=MONTHS,default=1)
    begin_year = models.IntegerField(default=1)

    def __str__(self):
        return '"%s" [digital] of user "%s"' %(self.token, self.customer)
    def __unicode__(self):
        return self.__str__()



class MechanicsWaterDevice(models.Model,WaterDeviceMixin):
    # customer = models.ForeignKey(Customer,related_name='mechanics_water_devices')
    token = models.CharField(default='',max_length = 255)
    active = models.BooleanField(default=False)

    begin_value = models.IntegerField(default=0)

    begin_month = models.IntegerField(choices=MONTHS,default=1)
    begin_year = models.IntegerField(default=1)

    def __str__(self):
        return '"%s" [mechanics] of user "%s"' %(self.token, self.customer)
    def __unicode__(self):
        return self.__str__()



class WaterContractType(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255,unique=True)
    def __str__(self):
        return '%s'%self.name
    def __unicode__(self):
        return self.__str__()

class WaterContractManager(models.Manager):
    def contract_for_customer_at(self,customer=None,month=None,year=None):
        begin_time_lte = Q(begin_time__year__lte=year) | (Q(begin_time__year = year) & Q(begin_time__month__lte=month))
        end_time_gte = Q(end_time__year__gte = year) | (Q(end_time__year = year) & Q(end_time__month__gte=month))

        contracts = self.filter(begin_time_lte,Q(end_time = None) | end_time_gte,customer=customer)

        if contracts.count() > 0 :
            return contracts[0]
        else:
            return None

class WaterContract(models.Model):

    objects = WaterContractManager()

    customer = models.ForeignKey(Customer,related_name='water_contracts')
    type = models.ForeignKey(WaterContractType,related_name='contracts')

    begin_time = models.ForeignKey(Month,null=True,related_name='begin_of_water_contracts')
    end_time = models.ForeignKey(Month,null=True,related_name='end_of_water_contracts')

    digital_device = models.ForeignKey(DigitalWaterDevice,null=True,related_name='contracts')
    mechanics_device = models.ForeignKey(MechanicsWaterDevice,null=True,related_name='contracts')

    def __str__(self):
        return '%s is %s, begin: %s, end: %s' % (self.customer,self.type,self.begin_time,self.end_time)
    def __unicode__(self):
        return self.__str__()

    def is_active(self):
        now = datetime.datetime.now()
        current_month = now.month
        current_year = now.year

        if current_year < self.begin_time.year:
            return False
        if current_year == self.begin_time.year and current_month < self.begin_time.month:
            return False

        if self.end_time:
            if current_year > self.end_time.year:
                return False
            if current_year == self.end_time.year and current_month > self.end_time.month:
                return False
        return True




class DigitalWaterDeviceCollect(models.Model):

    time = models.ForeignKey(Month)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    device = models.ForeignKey(DigitalWaterDevice,related_name='collects')
    value = models.IntegerField(default=0)

    def __str__(self):
        return 'month "%s", value "%s",device "%s"'% (self.time.month,self.value,self.device)
    def __unicode__(self):
        return self.__str__()


class MechanicsWaterDeviceCollect(models.Model):

    time = models.ForeignKey(Month)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    device = models.ForeignKey(MechanicsWaterDevice,related_name='collects')
    image = models.ImageField(upload_to='mechanics_water_device_collect_images',null=True)
    value = models.IntegerField(default=0)

    def __str__(self):
        return 'month "%s", value "%s",device "%s"'% (self.time.month,self.value,self.device)
    def __unicode__(self):
        return self.__str__()




class DigitalWaterDeviceUsed(models.Model):

    time = models.ForeignKey(Month)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    device = models.ForeignKey(DigitalWaterDevice,related_name='per_months')
    collect = models.ForeignKey(DigitalWaterDeviceCollect,related_name='collect_of',null=True)
    collect_before = models.ForeignKey(DigitalWaterDeviceCollect,related_name='collect_before_of',null=True)
    used = models.IntegerField(default=0)

    def __str__(self):
        return 'month "%s", used "%s",device "%s"'% (self.time.month,self.used,self.device)
    def __unicode__(self):
        return self.__str__()

class MechanicsWaterDeviceUsed(models.Model):

    time = models.ForeignKey(Month)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    device = models.ForeignKey(MechanicsWaterDevice,related_name='per_months')
    collect = models.ForeignKey(MechanicsWaterDeviceCollect,related_name='collect_of',null=True)
    collect_before = models.ForeignKey(MechanicsWaterDeviceCollect,related_name='collect_before_of',null=True)
    used = models.IntegerField(default=0,null=True)

    def __str__(self):
        return 'month "%s", used "%s",device "%s"'% (self.time.month,self.used,self.device)
    def __unicode__(self):
        return self.__str__()



class WaterPriceConfig(models.Model):
    NOT_SET = -1
    time = models.ForeignKey(Month)

    contract_type = models.ForeignKey(WaterContractType,related_name='price_configs')

    default_price = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-time__month','-time__year')

    def __str__(self):
        return ' %s/%s : %s, and %s other'%(self.month,self.year,self.default_price,self.prices.count())
    def __unicode__(self):
        return self.__str__()

    def total(self,used):
        s = 0

        for p in self.prices.all():
            if p.is_lt:
                if used <= p.max_value:
                    s += used * p.price
                elif used > p.max_value:
                    s += p.max_value * p.price
            elif p.is_range:
                if used >= p.min_value and used <= p.max_value:
                    s += (used - p.min_value +1) * p.price
                elif used > p.max_value:
                    s += (p.max_value - p.min_value +1) * p.price
            elif p.is_gt:
                if used >= p.min_value:
                    s += (used - p.min_value +1) * p.price
            else:
                pass

        return s

    def used_prices(self,used):

        result = []

        for p in self.prices.all():
            if p.is_lt:
                if used <= p.max_value:
                    result.append( (p,used, used * p.price))
                elif used > p.max_value:
                    result.append((p,p.max_value,p.max_value * p.price))
                else:
                    result.append((p,0,0))
            elif p.is_range:
                if used >= p.min_value and used <= p.max_value:
                    u = used - p.min_value +1
                    result.append((p,u,u * p.price))
                elif used > p.max_value:
                    u = p.max_value - p.min_value +1
                    result.append((p,u,u * p.price))
                else:
                    result.append((p,0,0))

            elif p.is_gt:
                if used >= p.min_value:
                    u = used - p.min_value +1
                    result.append((p,u,u * p.price))
                else:
                    result.append((p,0,0))


        return result

class WaterPrice(models.Model):

    NOT_SET = -1

    config = models.ForeignKey(WaterPriceConfig,related_name='prices')
    min_value = models.IntegerField(default=NOT_SET)
    max_value = models.IntegerField(default=NOT_SET)
    price = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('min_value','max_value')

    def __str__(self):
        return '"%s" - "%s" : "%s" VND' %(self.min_value,self.max_value)
    def __unicode__(self):
        return self.__str__()

    @property
    def is_lt(self):
        return self.min_value == self.NOT_SET and self.max_value != self.NOT_SET

    @property
    def is_range(self):
        return self.min_value != self.NOT_SET and self.max_value != self.NOT_SET

    @property
    def is_gt(self):
        return self.min_value != self.NOT_SET and self.max_value == self.NOT_SET

class WaterBill(models.Model):
    time = models.ForeignKey(Month)

    customer = models.ForeignKey(Customer,related_name='water_bills')

    digital_water_device_used = models.ForeignKey(DigitalWaterDeviceUsed,null=True)
    mechanics_water_device_used = models.ForeignKey(MechanicsWaterDeviceUsed,null=True)

    used = models.IntegerField(default=0)
    price_config = models.ForeignKey(WaterPriceConfig,related_name='water_bills')
    total = models.IntegerField(default=0)

    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-time__year','-time__month')

    def __str__(self):
        return '%s - %s, %s, used "%s", price "%s", total: "%s"' % (self.time.month,self.time.year,self.customer,self.used,self.price,self.total)
    def __unicode__(self):
        return self.__str__()

    def used_prices(self):
        return self.price_config.used_prices(self.used)

class IssueMessage(models.Model):
    customer = models.ForeignKey(Customer,related_name='issue_messages')
    title = models.CharField(max_length = 255)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '"%s", customer "%s", title "%s"' %(self.created_at,self.customer,self.title)
    def __unicode__(self):
        return self.__str__()

class AppRate(models.Model):
    RATES = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    )
    customer = models.OneToOneField(Customer,related_name='app_rate')
    rate = models.IntegerField(choices=RATES,default=5)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated_at',)

    def __str__(self):
        return '"%s" sao, "%s"' %( self.rate,self.message)
    def __unicode__(self):
        return self.__str__()
