from django.contrib import admin

from products.models import *
admin.site.register([StatusMaster,Product,Inventory,Channel,Alert])