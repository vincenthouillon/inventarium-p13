from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Equipment, Room, Residence, CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Form used to register a user."""

    terms = forms.BooleanField(
        error_messages={
            'required': 'Vous devez accepter les conditions d\'utilisation'},
        label="J'accepte les <a href='./terms/' target='_blank'> conditions \
            d\'utilisation.</a>"
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'last_name', 'first_name',
                  'password1', 'password2', 'terms', )


class CustomUserChangeForm(UserChangeForm):
    """Form used to update account a user."""

    class Meta:
        model = CustomUser
        fields = ('last_name', 'first_name', 'email', )


class ContactForm(forms.Form):
    from_email = forms.EmailField(label='Adresse électronique', required=True)
    subject = forms.CharField(label='Sujet', required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


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
