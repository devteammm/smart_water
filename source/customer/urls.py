from django.conf.urls import url
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^$',home),
    url(r'^issue_message$',issue_message),
    url(r'^contact$',contact),
    url(r'^rate$',rate),
]
