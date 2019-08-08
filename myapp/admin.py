from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Category, CustomUser, Equipment, Residence, Room

# Register your models here.
admin.site.register((Equipment, Room, Residence, Category, ))


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'last_name', 'first_name', 'is_staff',
                    'is_active', 'is_superuser')
    list_filter = ('is_superuser', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('last_name', 'first_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
        ('Informations personnelles', {'fields': ('last_name', 'first_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')})
    )
    search_fields = ('email', 'last_name', 'first_name')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
