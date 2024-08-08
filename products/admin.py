from django.contrib import admin

from products.models import *
admin.site.register([StatusMaster,Product,Device,Channel,Alert])