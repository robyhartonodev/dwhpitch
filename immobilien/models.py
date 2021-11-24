from django.db import models
from django.db.models.fields import CharField

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

class Country(models.Model):
    name=models.CharField(max_length=255, unique=True, default='Germany')
    code=models.CharField(max_length=255, unique=True, default='de')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Zip(models.Model):
    number=models.IntegerField()
    country=models.ForeignKey(Country, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Address(models.Model):
    street_name=models.CharField(max_length=255)
    street_details=models.CharField(max_length=255)
    zip=models.ForeignKey(Zip, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PropertyDetail(models.Model):
    description=models.TextField(default='description')
    address=models.ForeignKey(Address, on_delete=models.CASCADE)
    details_url=models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Property(models.Model):
    source=models.ForeignKey(Source, on_delete=models.CASCADE)
    property_type=models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    acquisition_type=models.ForeignKey(AcquisitionType, on_delete=models.CASCADE)
    detail=models.ForeignKey(PropertyDetail, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
