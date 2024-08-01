from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from operations.models import *
from operations.forms import ClientForm,InventoryForm,ProductForm,TransactionForm
from django.views.generic import FormView, CreateView,ListView,TemplateView,UpdateView
from django.utils.timezone import now
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from operations.serializers import ClientSerializer,InventorySerializer
from rest_framework.response import Response

from rest_framework import status
from django.contrib.auth.models import User
from datetime import date,time, timedelta, datetime
from django.views.generic import DetailView
from datetime import datetime
from django.db.models import Q, Sum, F, Count, Max
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *


class HomeTemplateView(TemplateView):
    template_name='operations/home.html' 


class CreateInventoryView(LoginRequiredMixin,FormView):  #Inventory creation
    template_name="operations/create_inventory.html"
    form_class=InventoryForm
    success_url="/operations/inventorylist"
    
    def form_valid(self,form):
        user = self.request.user
        object = form.save(commit=False)
        object.created_by = user
        object.updated_by = user
        object.status="Allocated"
        object.save()
        
        messages.success(self.request, (
            f'Inventory {object} has been created.'))
        
        return super().form_valid(form)


class InventoryEditView(LoginRequiredMixin, UpdateView):  #Inventory updation
    model = Inventory
    template_name = 'operations/edit_inventory.html'
    form_class = InventoryForm
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        self.object.save()
        messages.success(self.request, (
            f'inventory {self.object} has been updated successfully.'))
        return redirect('operations:inventorylist') 


@login_required    
def InventoryMgntList(request):                       #Inventory list
    objects=Inventory.objects.all()
    context={"objects":objects}
    return render(request,'operations/inventory_list.html',context)  


@login_required
def IoTMgntList(request):                             #IoT Mgnt list
    iot_device=Inventory.objects.raw("SELECT * FROM operations_Inventory")
    context={"objects":iot_device}
    return render(request,'operations/iot_mgnt_list.html',context)

class CreateIotMgntView(LoginRequiredMixin,FormView):    # IoT Mgnt create creation
    template_name="operations/create_iot_mgnt.html"
    form_class=InventoryForm
    success_url="/operations/iotmgntlist"
    
    def form_valid(self,form):
        user = self.request.user
        object = form.save(commit=False)
        object.created_by = user
        object.updated_by = user
        object.save()
        messages.success(self.request, (
            f'IoTMgnt {object} has been created.'))
        return super().form_valid(form)


class CreateClientView(LoginRequiredMixin,FormView):    # Client creation
    template_name="operations/create_client.html"
    form_class=ClientForm
    success_url="/operations/clients"
    
    def form_valid(self,form):
        user = self.request.user
        object = form.save(commit=False)
        object.created_by = user
        object.updated_by = user
        object.save()
        messages.success(self.request, (
            f'Client {object} has been created.'))
        return super().form_valid(form)


class ClientEditView(LoginRequiredMixin, UpdateView):           # Client updation
    model = Client
    template_name = 'operations/edit_client.html'
    form_class = ClientForm
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        self.object.save()
        messages.success(self.request, (
            f'client {self.object} has been updated successfully.'))
        return redirect('operations:clients')   


@login_required
def ClientList(request):                                   # Client list
    #objects=Client.objects.all()
    objects=Client.objects.raw("SELECT * FROM operations_Client")
    context={"objects":objects}
    return render(request,'operations/client_list.html',context)


class CreateProductView(LoginRequiredMixin,FormView):         # Product creation
    template_name="operations/create_product.html"
    form_class=ProductForm
    success_url="/operations/products"
    
    def form_valid(self,form):
        user = self.request.user
        object = form.save(commit=False)
        object.created_by = user
        object.updated_by = user
        object.save()
        messages.success(self.request, (
            f'Product {object} has been created.'))
        
        return super().form_valid(form)


class ProductEditView(LoginRequiredMixin, UpdateView):        # Product updation
    model = Product
    template_name = 'operations/edit_product.html'
    form_class = ProductForm
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        self.object.save()
        messages.success(self.request, (
            f'Product {self.object} has been updated successfully.'))
        return redirect('operations:products')


@login_required                                         # Products list
def ProductMgntList(request):
    #object.updated_at=request.user
    #object.updated_by=request.user
    
    objects=Product.objects.all()
    context={"objects":objects}
    return render(request,'operations/product_list.html',context) 


@login_required 
def user_list(request):                                    # User list
    objects=User.object.all()
    context={"objects":objects}
    return render(request,'accounts/userlist.html',context)


class CreateTransactionView(LoginRequiredMixin,FormView):      # Transaction creation
    template_name='operations/create_transaction.html'
    model=Transaction
    success_url="/operations/addtransaction"
    form_class=TransactionForm
    
    def form_valid(self,form):
        user=self.request.user
        object=form.save(Commit=False)
        object.updated_by=user
        object.created_by=user
        object.save()
        messages.success(self.request, (
            f'Transaction {object} has been created.'))
        return super().form_valid(form)
        
        
@login_required
def transaction_list(request):#for all transactions on today
    
    
    
    objects_today=Transaction.objects.filter(date_time__date = date.today()).order_by('inventory__name','-date_time') # for all transactions
    context={"objects":objects_today}
    return render(request,'operations/transaction_list.html',context)
    
    
@login_required    
def transaction_all_latest(request):            # Today's latest transactions
   
    objects_today = Transaction.objects.filter().order_by('inventory__name','-date_time')
            # query = self.model.objects.select_related('created_by').filter(
            # **searchParams).annotate(num_invites=Count('invites'))
    "select id"        
    result_objects = []
    inventory_names_set=set()
    for _ in objects_today:
        if _.inventory.name not in inventory_names_set:
            result_objects.append(_)
            inventory_names_set.add(_.inventory.name)
    context={"objects":result_objects}
    return render(request,'operations/transaction_list.html',context)


@login_required               
def all_machines(request):                    #All machines details
    object=0
    #objects=Machine.objects.all()
    objects=Transaction.objects.filter().order_by('inventory__name','-date_time')
    result_objects = []
    inventory_names_set=set()
    for _ in objects:
        if _.inventory.name not in inventory_names_set:
            result_objects.append(_)
            inventory_names_set.add(_.inventory.name)
        today=date.today()    
        print(today)
       
    context={"objects":result_objects}
    
    return render(request,'operations/machinelist.html',context)


def machine_data_history_view(request,id):           # selected machine data history
    context=dict
    objects=Transaction.objects.filter(inventory__id=id)
    #objects=Transaction.inventory.name.objects.get(id=id)
    print(objects)
    context={"objects":objects}
    return render(request,'operations/machine_history_data.html',context)

@csrf_exempt
def dump_data_view(request):
    dumpdata=DumpData()
    if request.method=='POST':
        dumpdata.data=request.body
        dumpdata.save()
    return JsonResponse(data={"dd":"great"})    
        
    
    

@csrf_exempt
#@login_required
def convert_dump_data_to_model(request):
    if request.method=='POST':
        dump_data=json.loads(request.body)
    #dump_data = {"id":"TUSTEMCN2023070003","client":"Apollo Hospital","machine serial number":"CBM551010","process count":"123","start time":"15:58:18","temperature":"35.5","result":"Standard S Complete","deviceTime":"2023-08-08 15:57:32","vacuume time":"15:58:18","finish time":"15:58:18","total time":"15:58:18","sterilizing":"15:58:18","pressure":"12","initializing":"15:58:18"}

    transaction = Transaction()
   
    
    try:
        inventory_id = dump_data['id']
        inventory = Inventory.objects.get(name= inventory_id)
        transaction.inventory = inventory
        client = Client.objects.get(name=dump_data['client'])
        transaction.client=client
        transaction.result = ResultTypeMaster.objects.get(name = dump_data['result'])
        transaction.process_count = dump_data['process count']
        transaction.date_time = dump_data['deviceTime']
        transaction.start_time =dump_data['start time']
        transaction.vacuum_time=dump_data["vacuume time"]
        transaction.finish_time=dump_data["finish time"]
        transaction.total_time=dump_data["total time"]
        transaction.initializing=dump_data["initializing"]
        transaction.sterilizing=dump_data["sterilizing"]
        transaction.pressure=dump_data["pressure"]
        transaction.temperature=dump_data["temperature"]
        transaction.save()
        return JsonResponse(data={"dd":"great"})
    except Exception as e:
        print("exception", e)        
    
    