from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
@api_view(['post'])
@permission_classes([AllowAny])
def register_user_view (request) :
    print(request.data)
    serializer = UserRegisterSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "message" : _("the new user was created successfuly"),
            "user" : {
                "id" : user.id,
                "nom" : user.last_name,
                "prenom" : user.first_name,
                "telephone" : user.telephone,
                "email" : user.email,
                "role" : user.role
            }
        }, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['post'])
@permission_classes([AllowAny])

def user_login_view (request) :
    serializer = UserLoginSerializer(data = request.data, context = {'request' : request})

    if serializer.is_valid() :
        user = serializer.validated_data['user']
        token = RefreshToken.for_user(user)

        return Response({
            "token" : str(token.access_token),
            "refresh" : str(token),
            "user" : user.id
        }, status=status.HTTP_202_ACCEPTED)
    
    return Response({
        "error" : _('invalid credentials')
    }, status=status.HTTP_400_BAD_REQUEST)