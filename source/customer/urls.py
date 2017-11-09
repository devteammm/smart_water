from django.conf.urls import url
from django.contrib import admin
from .views import *

app_name='customer'

urlpatterns = [
    url(r'^$',home,name='home'),
    url(r'^device_management$',device_management,name='device_management'),
    url(r'^device_info/(?P<device_type>\w+)/(?P<device_token>\w+)',device_info,name='device_info'),
    url(r'^update_mechanics_device_value/(?P<device_token>\w+)',update_mechanics_device_value,name='update_mechanics_device_value'),
    url(r'^api_parse_image_device_value$',api_parse_image_device_value,name='api_parse_image_device_value'),
    url(r'^price_info$',price_info,name='price_info'),
    url(r'^issue_message$',issue_message,name='issue_message'),
    url(r'^contact$',contact,name='contact'),
    url(r'^rate$',rate,name='rate'),
]
