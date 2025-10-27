from django.shortcuts import render
from .serializers import ContractSerializer
from .models import Contract
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from authentification.permissions import IsAdmin, IsManager
from rest_framework.response import Response
from rest_framework import status
from django.dispatch import receiver
from django.core.mail import send_mail, BadHeaderError
import smtplib
from authentification.models import User
from django.conf import settings
from company.serializers import CompanySerializer

# Create your views here.

@api_view(['post'])
@permission_classes([AllowAny])
def createContract (requst) :
    serializer = ContractSerializer(data=requst.data,context = {"request" : requst})

    if serializer.is_valid() :
        contract = serializer.save()
       
        company = contract.product.company
        managers = company.managers.all()
        manager_email = list(managers.values_list('email', flat=True))

        try :

            send_mail(
                "New Contract Signed",
                f"For product {contract.product.name}. \nSigned by {contract.client.get_full_name()}\n Phone : {contract.client.telephone}\nEmail : {contract.client.email}\nDate : {contract.signed_at.strftime('%Y-%m-%d %H:%M:%S')} ",
                settings.DEFAULT_FROM_EMAIL,
                manager_email
            )
        except (BadHeaderError, smtplib.SMTPException) as e :
            return Response({
                "message" : f"error while sending the email\n{e}"
            })

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
       
@api_view(['put'])
@permission_classes([IsAdmin | IsManager])

def updateContract (request, pk) :
    try :
        contract = Contract.objects.get(pk=pk)
    except Contract.DoesNotExist :
        return Response ({
            "error" : "Contract does not xist"
        }, status=status.HTTP_404_NOT_FOUND)
    
    if contract.product.company == request.user.company :
        contract.viewed = False
        contract.save()
        serializer = ContractSerializer(contract, data = request.data , partial=True)
        if serializer.is_valid() :
            contract = serializer.save()
            client_email = contract.client.email
            
            try :
                send_mail(
                    f"Your Contract With {contract.product.company.name} has been updated",
                    f"Your contract is {contract.status.capitalize()}",
                    settings.DEFAULT_FROM_EMAIL,
                    [client_email]
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            except (BadHeaderError, smtplib.SMTPException) as e :
                return Response({
                    "message" : f"error while sending the email\n{e}"
                })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        "message" : "you are not autherized to do that"
    }, status=status.HTTP_403_FORBIDDEN)
    
        

@api_view(['get'])
@permission_classes([AllowAny])
def getAllContracts (request) :
    if request.user.role == 'ADMIN' :
        contracts = Contract.objects.all()
        serializer = ContractSerializer(contracts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.user.role == 'MANAGER' :
        contracts = Contract.objects.filter(product = request.user.company)
        serializer = ContractSerializer(contracts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    


@api_view(['GET'])
@permission_classes([AllowAny])

def getUserContracts (request, user_id) :
    try : 
        user = User.objects.get(id=user_id)
    except user.DoesNotExist :
        return Response({
            "error" : "User does not exist"
        }, status=status.HTTP_404_NOT_FOUND)
    

    contracts = Contract.objects.filter(client = user)
    if contracts :
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({
        "error" : "User has no contracts"
    }, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([AllowAny])

def contractCompany (request, contract_id) :
    try:
        contract = Contract.objects.get(pk=contract_id)
    except Contract.DoesNotExist:
        return Response({"error": "Contract does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    company = contract.product.company
    serializer = CompanySerializer(company, context={"request" : request})

    return Response (serializer.data, status=status.HTTP_200_OK)