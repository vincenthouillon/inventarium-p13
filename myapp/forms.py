from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Equipment, Room, Room_type

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
        fields = ('name', 'brand', 'model', 'date_purchase', 'lenght_warranty',
                  'note', 'picture', 'invoice', 'manual', 'active', 'room', 'category')


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name', 'picture', 'residence', 'room_type')

class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = Room_type
        fields = ('name',)
