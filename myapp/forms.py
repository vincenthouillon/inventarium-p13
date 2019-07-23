from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Equipment, Room, Residence

# User registration form
class UserRegisterForm(UserCreationForm):
    """Form used to register a user."""
    email = forms.EmailField(
        label="Adresse électronique",
        max_length=255,
        required=True)

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name',
                  'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email')


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ['residence']


class ResidenceForm(forms.ModelForm):
    class Meta:
        model = Residence
        exclude = ['user']

