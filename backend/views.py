from django.shortcuts import render

# Create your views here.
from backend.models import Car


def home(request):
    return render(request, "index.html", {})

def getCars(request):
    cars = Car.objects.all()


