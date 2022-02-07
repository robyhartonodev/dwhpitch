from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Property)
admin.site.register(Source)
admin.site.register(PropertyType)
admin.site.register(PropertyAcquisitionType)
admin.site.register(PropertyIdentifier)
admin.site.register(State)
admin.site.register(Zip)
admin.site.register(Address)
admin.site.register(PropertyDetail)
admin.site.register(PropertyVendor)
admin.site.register(PropertyFeature)
admin.site.register(PropertyImage)
admin.site.register(PropertyPriceType)