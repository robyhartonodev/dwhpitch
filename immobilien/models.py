from django.db import models

# Create your models here.
class Source(models.Model):
    name=models.CharField(max_length=255, unique=True)
    base_url=models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PropertyType(models.Model):
    name=models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AcquisitionType(models.Model):
    name=models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class State(models.Model):
    name=models.CharField(max_length=255, unique=True)
    state_code=models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class City(models.Model):
    name=models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Zip(models.Model):
    code=models.CharField(max_length=8)
    city=models.ForeignKey(City, on_delete=models.CASCADE)
    state=models.ForeignKey(State, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Address(models.Model):
    street_name=models.CharField(max_length=255)
    street_details=models.CharField(max_length=255, blank=True, null=True)
    zip=models.ForeignKey(Zip, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PropertyDetail(models.Model):
    title=models.CharField(max_length=255, default='default')
    description=models.TextField(default='description')
    other=models.TextField(default='other')
    address=models.ForeignKey(Address, on_delete=models.CASCADE)
    details_url=models.URLField(blank=True, null=True)
    price=models.JSONField(blank=True, null=True)
    size_and_condition=models.JSONField(blank=True, null=True)
    energy=models.JSONField(blank=True, null=True)
    features=models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Property(models.Model):
    source=models.ForeignKey(Source, on_delete=models.CASCADE)
    property_type=models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    acquisition_type=models.ForeignKey(AcquisitionType, on_delete=models.CASCADE)
    detail=models.ForeignKey(PropertyDetail, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
