from django.conf.urls import url, include,static
from django.conf import settings

from django.contrib import admin

from main import views as main_views
from customer.views import api_update_digital_device_value

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('sysauth.urls')),
    url(r'^customer/', include('customer.urls')),
    url(r'^water_staff/', include('water_staff.urls')),

    url(r'^water_device/digital/(?P<device_token>\w+)/(?P<value>[0-9]+)$',api_update_digital_device_value),
    url(r'^$',main_views.home),
]+ static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
