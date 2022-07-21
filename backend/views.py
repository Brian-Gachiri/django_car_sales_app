from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.auth import getToken
from backend.models import Car, Brand, Buyer, Favorites
from backend.serializers import CarSerializer, BrandSerializer, CustomFavoriteSerializer


def home(request):
    return render(request, "index.html", {})


class CarView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class BrandView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getFavorites(request):
    request_token = getToken(request)

    token = Token.objects.filter(key=request_token).first()
    user = Buyer.objects.filter(pk=token.user_id).first()

    favorites = Favorites.objects.filter(buyer=user).prefetch_related('car').only('id')

    for favorite in favorites:
        favorite.car_name = favorite.car.name
        favorite.car_id = favorite.car_id
        favorite.image = favorite.car.image.url

    data = CustomFavoriteSerializer(favorites, many=True)

    return Response(data.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def addToFavorites(request, id):
    request_token = getToken(request)

    token = Token.objects.filter(key=request_token).first()
    user = Buyer.objects.filter(pk=token.user_id).first()
    car = Car.objects.filter(pk=id).first()

    isFavorited = Favorites.objects.filter(buyer=user, car=car).first()

    if isFavorited:

        context = {
            'success': 0,
            'message': "Car removed from favorites"
        }
        isFavorited.delete()
        return Response(context, status=status.HTTP_200_OK)

    else:
        Favorites.objects.create(
            buyer=user,
            car=car
        )
        context = {
            'success': 1,
            'message': "Car added to favorites"
        }

        return Response(context, status=status.HTTP_200_OK)
