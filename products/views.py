from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *

class HomepageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'products/home.html'


"""
{"id":"TU2HT0320240002" , "values":{"1":"-23.23" , "2":"-22.31" , "10":"1" , "11":"0" , "31":"90.88" , "32":"91.25" , "33":"0" , "34":"0"} , "deviceTime":"2024-08-01 17:24:00"}
"""    
# Import necessary library
import json

# JSON data
json_data = '{"id":"TU2HT0320240002", "values":{"1":"-23.23", "2":"-22.31"}, "deviceTime":"2024-08-01 17:24:00"}'

# Parse JSON data
data = json.loads(json_data)

# Store data in dummy variables
record_id = data['id']
value_1 = float(data['values']['1'])
value_2 = float(data['values']['2'])
device_time = data['deviceTime']

# Print the variables to verify
print(f"Record ID: {record_id}")
print(f"Value 1: {value_1}")
print(f"Value 2: {value_2}")
print(f"Device Time: {device_time}")


@csrf_exempt
#@login_required
def convert_dump_data_to_model(request):
    # dump_data={"id":"TU2HT0320240002" , "values":{"1":"-7.43" , "2":"-15.83"} , "deviceTime":"2024-08-08 18:26:55"}
    if request.method=='POST':
        dump_data=json.loads(request.body)
        reading=TemperatureReading()
        Device.name=dump_data['id']
        Channel.objects.get(label=dump_data['values']['1'])
        Channel.objects.get(label=dump_data['values']['1'])
        reading.received_at=dump_data['deviceTime']
      
   

