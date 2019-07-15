from django.contrib import admin
from .models import (Equipment, Room, Room_type, Residence, Category)

# Register your models here.
admin.site.register((Equipment, Room, Room_type, Residence, Category))