from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Buyer(User):
    image = models.ImageField(upload_to="profile", null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True)
    location = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username

class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField()

    def __str__(self):
        return self.name

class Car(models.Model):
    MANUAL = 0
    AUTOMATIC = 1
    TRANSMISSIONS = (
        (MANUAL, "Manual"),
        (AUTOMATIC, "Automatic")
    )
    name = models.CharField(max_length=100, default="")
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

    def __str__(self):
        return self.name

class CarImage(models.Model):
    image = models.ImageField()
    car = models.ForeignKey(Car, on_delete=models.ForeignKey)

    def __str__(self):
        return self.car

##TODO: Favorites (Wishlists), Bids, Orders