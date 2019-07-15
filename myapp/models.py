# https://docs.djangoproject.com/fr/2.2/topics/db/models/
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Residence(models.Model):
    """Residence data table."""
    name = models.CharField(
        "nom de la résidence", max_length=45)
    adress = models.CharField("adresse", max_length=80, null=True)
    zip_code = models.IntegerField("code postal", null=True)
    city = models.CharField("ville", max_length=45, null=True)
    # Relation ################################################################
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="utilisateur")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "résidence"


class Room_type(models.Model):
    """Data table of the room types of the house"""
    name = models.CharField(
        "type de pièce", max_length=80, unique=True)
    default_picture = models.ImageField(upload_to='room/default',
        null=True, verbose_name="image par défaut", default="default/default.jpg")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "type de pièce"


class Room(models.Model):
    """Data table of rooms in the house."""
    name = models.CharField(
        "Nom de la pièce", max_length=80, unique=True)
    picture = models.ImageField(
        upload_to="rooms/picture", null=True, blank=True, verbose_name="Image")
    # Relation ################################################################
    residence = models.ForeignKey(
        Residence, on_delete=models.CASCADE, verbose_name="résidence")
    room_type = models.ForeignKey(
        Room_type, on_delete=models.CASCADE, verbose_name="type de pièce")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "pièce"


class Category(models.Model):
    """Category data table."""
    name = models.CharField("catégorie", max_length=25, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "catégorie"


class Equipment(models.Model):
    """Data table of the equipment of the house."""
    name = models.CharField("nom de l'équipement", max_length=80)
    brand = models.CharField("marque", max_length=30)
    model = models.CharField("modèle", max_length=40)
    date_purchase = models.DateField(
        "date d'achat", blank=True, default=datetime.now)
    lenght_warranty = models.IntegerField(
        "durée de garantie", null=True, help_text="Durée exprimée en mois", default="48")
    note = models.TextField("remarque", null=True)
    picture = models.ImageField(
        upload_to="equipments/picture", null=True, blank=True, verbose_name="photo")
    invoice = models.FileField(
        upload_to="equipements/invoice", null=True, blank=True, verbose_name="facture")
    manual = models.FileField(upload_to="equipements/manual",
                              null=True, blank=True, verbose_name="mode d'emploi")
    active = models.BooleanField("Equipement actif", default=1)
    # Relation ################################################################
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, verbose_name="pièce")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="catégorie")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'équipement'
