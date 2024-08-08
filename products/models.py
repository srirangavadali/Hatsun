from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings




class BaseTimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BaseUserTrackedModel(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, default=None, on_delete=models.SET_NULL, related_name="created_%(class)s")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, default=None, on_delete=models.SET_NULL, related_name="updated_%(class)s")

    class Meta:
        abstract = True

class CommonMasterAbstract(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    is_active = models.BooleanField(default=True, verbose_name="Is Active", null=True)
  
    def __str__(self):
        return f"{self.name}"
    class Meta:
        abstract = True 

class StatusMaster(CommonMasterAbstract):
    pass

class ProductMaster(models.Model):
    name=  models.CharField(max_length=150, blank=False,unique=True) 
    is_active = models.BooleanField(null=True, default=True)
   
    class Meta:
        abstract=True
        

class Product(ProductMaster,BaseUserTrackedModel,BaseTimestampedModel):  #Product table
     def __str__(self):
        return f"{self.name}"       

class InventoryMaster(models.Model):
    name=models.CharField(max_length=150, blank=False)
    connection_name=models.CharField(max_length=150, blank=False)
    status=models.BooleanField(null=True, default=True)
    class Meta:
        abstract=True

class Device(InventoryMaster,BaseUserTrackedModel,BaseTimestampedModel):
     product = models.ForeignKey(Product,on_delete=models.CASCADE,null=False)
     def __str__(self):
        return f"{self.name}"

class ChannelMaster(models.Model):
    number=models.SmallIntegerField(null=False)
    label=models.CharField(max_length=150, blank=False)
    is_display=models.BooleanField(null=True, default=True)
    display_order=models.SmallIntegerField(null=False)
    unit_of_measure=models.CharField(max_length=150, blank=True,null=True)
    min_value=models.FloatField()
    max_value=models.FloatField()
    device=models.ForeignKey(Device,on_delete=models.CASCADE,null=False)
    class Meta:
        abstract=True

class Channel(ChannelMaster,BaseUserTrackedModel,BaseTimestampedModel):
    def __str__(self):
        return f"{self.label}"

class TemperatureReading(models.Model):
    value=models.FloatField()
    received_at=models.DateTimeField()
    channel=models.ForeignKey(Channel,on_delete=models.CASCADE,null=False)



class Alert(models.Model):
    name=  models.CharField(max_length=150, blank=False)
    connection_name=models.ForeignKey(Device,on_delete=models.CASCADE,null=False)
    


  

