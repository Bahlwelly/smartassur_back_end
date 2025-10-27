from django.shortcuts import render
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from .serializers import IPSerializer
from rest_framework import status
from .models import InsuranceProduct
from authentification.permissions import IsManager, IsAdmin
from rest_framework.permissions import AllowAny
from company.serializers import CompanySerializer

# Create your views here.
@api_view(['post'])
@permission_classes([IsManager | IsAdmin])
def createIP (request) :
    if not request.user.company :
        return Response ({
            "message" : "you are not assigned to a company"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    data = request.data.copy()
    data['company'] = request.user.company.id

    serializer = IPSerializer(data = data)
    if serializer.is_valid() :
        serializer.save(company = request.user.company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['put'])
@permission_classes([IsAdmin | IsManager])
def updateIP (request, pk) :
    try : 
        ip = InsuranceProduct.objects.get(pk=pk)
    except InsuranceProduct.DoesNotExist :
        return Response ({
            "error" : "Product doesn't exist"
        }, status=status.HTTP_404_NOT_FOUND)
    
    if ip.company == request.user.company :
        serializer = IPSerializer(ip, data = request.data, partial=True)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        "error" : "You are not allowed to change this"
    }, status=status.HTTP_403_FORBIDDEN)



@api_view(['get'])
@permission_classes([AllowAny])
def getAllIPs (request) :
    ips = InsuranceProduct.objects.all()
    serializer = IPSerializer(ips, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['get'])
@permission_classes([AllowAny])
def getIPDetails (request, pk) :
    try :
        ip = InsuranceProduct.objects.get(pk=pk)
    except InsuranceProduct.DoesNotExist :
        return Response ({
            "error" : "Product does not xist"
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = IPSerializer(ip)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['delete'])
@permission_classes([IsAdmin | IsManager])
def deleteIP (request, pk) :
    try :
        ip = InsuranceProduct.objects.get(pk=pk)
    except InsuranceProduct.DoesNotExist :
        return Response ({
            "error" : "Product does not xist"
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.user.company == ip.company :    
        ip.delete()

        return Response ({
            "message" : "Product deleted"
        }, status=status.HTTP_200_OK)
    
    return Response ({
        "error" : "You are not allowed to delete this"
    }, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([AllowAny])
def getIPCompany (request, product_id) :
    try :
        ip = InsuranceProduct.objects.get(pk=product_id)
    except InsuranceProduct.DoesNotExist : 
        return Response({"error" : "Product doesnt exist"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CompanySerializer(ip.company , context={"request" : request})
    return Response(serializer.data, status=status.HTTP_200_OK)