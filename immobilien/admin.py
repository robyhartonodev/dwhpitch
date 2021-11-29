from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Property)
admin.site.register(Source)
admin.site.register(PropertyType)
admin.site.register(PropertyAcquisitionType)
admin.site.register(Zip)
admin.site.register(Address)
admin.site.register(PropertyDetail)