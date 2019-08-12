# https://docs.djangoproject.com/fr/2.2/topics/db/models/
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from PIL import Image

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_name = models.CharField('nom', max_length=150, blank=True)
    first_name = models.CharField('prénom', max_length=150, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'utilisateur'


class Residence(models.Model):
    """ Residence data table. """
    name = models.CharField(
        "nom de la résidence", max_length=45)
    adress = models.CharField("adresse", max_length=80, null=True, blank=True)
    zip_regex = RegexValidator(
        regex=r'^\d{5}$',
        message="Le code postal doit être au format 99999, exemple : '75000'.")
    zip_code = models.CharField("code postal", validators=[
                                zip_regex],
                                max_length=5,
                                null=True,
                                blank=True)
    city = models.CharField("ville", max_length=45, null=True, blank=True)

    # user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, verbose_name="utilisateur")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name="utilisateur")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "résidence"


class Room(models.Model):
    """ Data table of rooms in the house. """
    name = models.CharField(
        "Nom de la pièce", max_length=80)
    picture = models.ImageField(
        upload_to="rooms/picture", null=True, blank=True, verbose_name="Image")

    residence = models.ForeignKey(
        Residence, on_delete=models.CASCADE, verbose_name="résidence")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "pièce"

    def save(self, **kwargs):
        super().save()

        if self.picture:
            img = Image.open(self.picture.path)
            if img.height > 400 or img.width > 400:
                output_size = (400, 400)
                img.thumbnail(output_size)
                img.save(self.picture.path)


class Category(models.Model):
    """ Category data table. """
    name = models.CharField("catégorie", max_length=25, unique=True)

    def __str__(self, **kwargs):
        return self.name

    class Meta:
        verbose_name = "catégorie"


class Equipment(models.Model):
    """
    Data table of the equipment of the house with automatic resizing of the
    images and restriction of the extension of the files to .pdf.
    """
    name = models.CharField("nom de l'équipement", max_length=80)
    brand = models.CharField("marque", max_length=30, null=True, blank=True)
    model = models.CharField("modèle", max_length=40, null=True, blank=True)
    price = models.DecimalField("prix", max_digits=6, decimal_places=2,
                                null=True, blank=True, default=0.00)
    date_purchase = models.DateField(
        "date d'achat", blank=True, default=datetime.now,
        help_text='Format date : 26/10/1985')
    length_warranty = models.IntegerField(
        "durée de garantie", null=True, help_text="Durée exprimée en mois",
        default="24", blank=True)
    note = models.TextField("note", null=True, blank=True)
    picture = models.ImageField(
        upload_to="equipments/picture", null=True, blank=True,
        verbose_name="photo")
    invoice = models.FileField(
        upload_to="equipments/invoice", null=True, blank=True,
        verbose_name="facture",
        help_text="Uniquement fichier PDF.",
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf'],
            message="Seul les fichiers .pdf sont acceptés.")])
    manual = models.FileField(
        upload_to="equipments/manual",
        null=True, blank=True,
        verbose_name="mode d'emploi",
        help_text="Uniquement fichier PDF.",
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf'],
            message="Seul les fichiers .pdf sont acceptés.")])
    is_active = models.BooleanField("Equipement actif", default=1)

    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, verbose_name="pièce")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="catégorie")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'équipement'

    def save(self, **kwargs):
        super().save()

        if self.picture:
            img = Image.open(self.picture.path)
            if img.height > 400 or img.width > 400:
                output_size = (400, 400)
                img.thumbnail(output_size)
                img.save(self.picture.path)
