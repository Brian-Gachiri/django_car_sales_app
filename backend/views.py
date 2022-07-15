from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView

from backend.models import Car, Brand
from backend.serializers import CarSerializer, BrandSerializer


def home(request):
    return render(request, "index.html", {})


class CarView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class BrandView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

