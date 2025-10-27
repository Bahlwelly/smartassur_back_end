from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdmin, IsManager
from .models import User

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
            "refresh_token" : str(token),
            "access_token" : str(token.access_token),
            "user" : user.id
        })

        return res
    
    return Response({
        "error" : _('invalid credentials')
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['get'])
@permission_classes([IsAdmin | IsManager])
def getuUsers (request) :
    if (request.user.role == 'admin') :
        users = User.objects.all();
        serializer = UserSerializer(users, many=True)
    else :
        if request.user.role == 'manager' and request.user.company :
            company = request.user.company
        else :
            user_contract = request.user.contracts.first()
            if not user_contract :
                return Response({"message" : "User has no contracts"}, status=status.HTTP_404_NOT_FOUND)
            company = user_contract.product.company
        
        users = User.objects.filter(contracts__product__company=company).distinct()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['get'])
@permission_classes([AllowAny])
def getUserDetails (request, pk) :
    try :
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except user.DoesNotExist :
        return Response({
            "message" : "User doesn't exist"
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['put'])
@permission_classes([AllowAny])
def updateUser (request, pk) :
    try : 
         user = User.objects.get(pk=pk)
    except user.DoesNotExist :
        return Response({
            "message" : "user doesnt exist"
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.user == user :
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid() :
            serializer.save()
            return Response({
                "message" : "user updated successfully"
            }, status=status.HTTP_200_OK)
        else :
            return Response ({
                "message" : "Invalid data"
            }, status=status.HTTP_400_BAD_REQUEST)
        
    else :
            return Response ({
                "message" : "Only the user can change its own data"
            }, status=status.HTTP_401_UNAUTHORIZED)
        


@api_view(['post'])
@permission_classes([AllowAny])
def logout (request) :
    refresh_token = request.data.get('refresh_token')
    if not refresh_token :
        return Response({"error" : "refresh token not found"}, status=status.HTTP_400_BAD_REQUEST)
    try :
        token = RefreshToken(refresh_token)
        token.blacklist()

    except TokenError as e :
        pass
    
    response = Response({"message": "logged out successfully"}, status=status.HTTP_200_OK)
    return response
