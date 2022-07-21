from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.models import Token

from backend.models import Buyer


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def loginUser(request):
    username = request.data.get("username")
    password = request.data.get("password")

    buyer = Buyer.objects.filter(username=username).first()
    username = buyer.username
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        context = {
            'error': 'Invalid Username or Password',
        }
        return Response(context, status=status.HTTP_401_UNAUTHORIZED)
    token, _ = Token.objects.get_or_create(user=user)
    context = {
        'token': token.key,
        'id': user.id,
        'username': username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number': buyer.phone_number,
        'address': buyer.location,
        'status': buyer.status
    }
    return Response(context,
                    status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def registerUser(request):
    phonenumber = request.data.get("number")
    password = request.data.get("password")
    email = request.data.get("email")
    name = request.data.get("name")
    location = request.data.get("location", "")

    if name is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_403_FORBIDDEN)

    # user = Buyer.objects.filter(username = name).first()
    error = validate_fields(name, email, phonenumber)

    if error:
        return Response({'error': error}, status=status.HTTP_403_FORBIDDEN)

    user = Buyer()
    user.username = name
    user.phone_number = phonenumber
    user.email = email
    user.location = location
    user.set_password(password)
    user.is_staff = False
    user.save()

    token, _ = Token.objects.get_or_create(user=user)
    context = {
        'token': token.key,
        'id': user.pk,
        'username': name,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number': phonenumber,
        'location': user.location
    }

    return Response(context,
                    status=status.HTTP_200_OK)


def getToken(request):
    r_token = request.META['HTTP_AUTHORIZATION']

    return r_token.split(' ', 1)[1]


def validate_fields(name, email,phone_number):
    name = Buyer.objects.filter(username=name).first()
    email = Buyer.objects.filter(email=email).first()
    phone_number = Buyer.objects.filter(phone_number=phone_number).first()

    if email:
        return 'This email is already taken'
    elif name:
        return 'Username already exists'
    elif phone_number:
        return 'This phone number is already taken'
    else:
        return
