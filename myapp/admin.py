from django.contrib import admin
from .models import (Equipment, Room, Residence, Category)

# Register your models here.
admin.site.register((Equipment, Room, Residence, Category))
