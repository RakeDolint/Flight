from django.contrib import admin
from FlightIndex.models import Flight,Airport,User,Passenger

# Register your models here.
admin.site.register([Flight,Airport,User,Passenger])