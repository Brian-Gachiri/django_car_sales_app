from rest_framework import serializers
from .models import *

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

class CustomFavoriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    car_name = serializers.CharField()
    image = serializers.CharField()
    car_id = serializers.IntegerField()
