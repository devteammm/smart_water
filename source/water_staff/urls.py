from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'water_staff'

urlpatterns = [
    url(r'^customer_management$',customer_management,name='customer_management'),
    url(r'^revenue_statistics$',revenue_statistics,name='revenue_statistics'),
]
