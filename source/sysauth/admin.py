from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(WaterCompany)
admin.site.register(WaterCompanyStaff)
admin.site.register(WaterDepartment)
admin.site.register(WaterDepartmentStaff)
