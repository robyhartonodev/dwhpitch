from django.db import models

class Source(models.Model):
    name=models.CharField(max_length=255, unique=True)
    base_url=models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class PropertyIdentifier(models.Model):
    identifier=models.CharField(max_length=255)
    source=models.ForeignKey(Source, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PropertyType(models.Model):
    name=models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PropertyAcquisitionType(models.Model):
    name=models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class State(models.Model):
    name=models.CharField(max_length=255, unique=True)
    state_code=models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Zip(models.Model):
    code=models.CharField(max_length=8)
    name=models.CharField(max_length=255, default="default")
    state=models.ForeignKey(State, on_delete=models.CASCADE)
    latitude=models.FloatField(blank=True, null=True)
    longitude=models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Address(models.Model):
    street_name=models.CharField(max_length=255, blank=True, null=True, default="default")
    street_details=models.CharField(max_length=255, blank=True, null=True, default="default")
    zip=models.ForeignKey(Zip, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PropertyVendor(models.Model):
    name=models.CharField(max_length=255, default="default", blank=True, null=True)
    telephone_number=models.CharField(max_length=255, default="default", blank=True, null=True)
    mobile_number=models.CharField(max_length=255, default="default", blank=True, null=True)
    email=models.EmailField(blank=True, null=True, default="default@mail.com")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PropertyFeature(models.Model):
    name=models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PropertyImage(models.Model):
    image_url=models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PropertyPriceType(models.Model):
    name=models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PropertyDetail(models.Model):
    title=models.CharField(max_length=255, default='default', blank=True, null=True)
    description=models.TextField(default='default', blank=True, null=True)
    other=models.TextField(default='default', blank=True, null=True)
    address=models.ForeignKey(Address, on_delete=models.CASCADE)
    details_url=models.URLField(blank=True, null=True)
    room_count=models.FloatField(blank=True, null=True)
    price_show=models.FloatField(blank=True, null=True)
    size_in_meter_square=models.FloatField(blank=True, null=True)
    vendor=models.ForeignKey(PropertyVendor, on_delete=models.CASCADE)
    features=models.ManyToManyField(PropertyFeature, blank=True, through='PropertyDetailFeature')
    images=models.ManyToManyField(PropertyImage, blank=True, through='PropertyDetailImage')
    detail_prices=models.ManyToManyField(PropertyPriceType, blank=True, through='PropertyDetailPrice')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PropertyDetailFeature(models.Model):
    detail=models.ForeignKey(PropertyDetail, on_delete=models.CASCADE)
    feature=models.ForeignKey(PropertyFeature, on_delete=models.CASCADE)

    class Meta:
        unique_together= (('detail', 'feature'))

class PropertyDetailImage(models.Model):
    detail=models.ForeignKey(PropertyDetail, on_delete=models.CASCADE)
    image=models.ForeignKey(PropertyImage, on_delete=models.CASCADE)

    class Meta:
        unique_together= (('detail', 'image'))

class PropertyDetailPrice(models.Model):
    detail=models.ForeignKey(PropertyDetail, on_delete=models.CASCADE)
    price_type=models.ForeignKey(PropertyPriceType, on_delete=models.CASCADE)
    value=models.FloatField(blank=True, null=True)

    class Meta:
        unique_together= (('detail', 'price_type'))

class Property(models.Model):
    property_identifier=models.ForeignKey(PropertyIdentifier, on_delete=models.CASCADE)
    property_type=models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    property_acquisition_type=models.ForeignKey(PropertyAcquisitionType, on_delete=models.CASCADE)
    property_detail=models.ForeignKey(PropertyDetail, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
