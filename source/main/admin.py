from django.contrib import admin
from .models import *

admin.site.register(DigitalWaterDevice)
admin.site.register(MechanicsWaterDevice)
admin.site.register(DigitalWaterDeviceCollect)
admin.site.register(MechanicsWaterDeviceCollect)
admin.site.register(WaterInfo)
