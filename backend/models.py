from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=100)

class Buyer(User):
    image = models.ImageField(upload_to="profile", null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True)
    location = models.TextField(null=True, blank=True)

class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField()

class Car(models.Model):
    MANUAL = 0
    AUTOMATIC = 1
    TRANSMISSIONS = (
        (MANUAL, "Manual"),
        (AUTOMATIC, "Automatic")
    )
    overview = models.TextField()
    horsepower = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField()
    model = models.CharField(max_length=100)
    fuel = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    color = models.CharField(max_length=15)
    transmission = models.IntegerField(choices=TRANSMISSIONS, default=AUTOMATIC)
    year_of_manufacture = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, null=True, blank=True)

class CarImage(models.Model):
    image = models.ImageField()
    car = models.ForeignKey(Car, on_delete=models.ForeignKey)

##TODO: Favorites (Wishlists), Bids, Orders