from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Equipment, Room, Residence


class UserRegisterForm(UserCreationForm):
    """Form used to register a user."""
    email = forms.EmailField(
        label="Adresse électronique",
        max_length=255,
        required=True)

    terms = forms.BooleanField(
        error_messages={
            'required': 'Vous devez accepter les conditions d\'utilisation'},
        label="J'accepte les <a href='./terms/' target='_blank'> conditions d\'utilisation.</a>"
    )

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name',
                  'email', 'password1', 'password2', 'terms')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        label="Adresse électronique",
        max_length=255)

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email')


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        exclude = ['room']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ['residence']


class ResidenceForm(forms.ModelForm):
    class Meta:
        model = Residence
        exclude = ['user']
