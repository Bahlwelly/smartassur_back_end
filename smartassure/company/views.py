from django.shortcuts import render
from .models import Company, InsuranceCategory, ManagerInvite
from .serializers import CompanySerializer, InsuranceCategorySerializer
from  rest_framework.decorators import api_view, permission_classes
from authentification.permissions import IsAdmin, IsManager, IsClient
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import smtplib
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from insuranceproduct.serializers import IPSerializer
from contract.serializers import ContractSerializer, Contract
from .translation import translate_text

# Create your views here.
@api_view(['post'])
@permission_classes([IsAdmin | IsManager])
def addCompanyView (request) :
    data = request.data.copy()
    name = data.get('name_original')
    description = data.get('description_original')

    if not name or not description :
        return Response({"message" : "the name and the description are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    translations = {
        'name_en' : translate_text(name, 'en'),
        'name_ar' : translate_text(name, 'ar'),
        'name_fr' : translate_text(name, 'fr'),

        'description_en' : translate_text(description, 'en'),
        'description_fr' : translate_text(description, 'fr'),
        'description_ar' : translate_text(description, 'ar'),
    }

    data.update({
        'description_en' : translations["description_en"],
        'description_fr' : translations["description_fr"],
        'description_ar' : translations["description_ar"],

        'name_en' : translations["name_en"],
        'name_fr' : translations["name_fr"],
        'name_ar' : translations["name_ar"],
    })


    serializer = CompanySerializer(data = data)

    if serializer.is_valid() : 
        company = serializer.save()
        request.user.company = company
        request.user.save()

        return Response({
            "message" : "new company added successfully",
            "company" : {
                "name_en" : company.name_en,
                "name_fr" : company.name_fr,
                "name_ar" : company.name_ar,
                "description_en" : company.description_en,
                "description_ar" : company.description_ar,
                "description_fr" : company.description_fr,
                "location" : company.location,
                "website" : company.website,
                "phone" : company.phone,
                "email" : company.email,
                "managers": [
                    {"id": u.id, "name": f"{u.first_name} {u.last_name}", "email": u.email} 
                    for u in company.managers.all()
                ],
                "categories" : [
                    {"id" : cat.id, "name" : cat.name}
                    for cat in company.categories.all()
                ]
            }
        }, status=status.HTTP_201_CREATED)
    return Response({
        "message" : "Error in the creation",
        "errors" : serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['put'])
@permission_classes([IsAdmin | IsManager])
def updateCompanyView (request, pk) :
    try : 
        comp = Company.objects.get(pk = pk)
    except Company.DoesNotExist :
        return Response({
            "error" : "not found"
        }, status=status.HTTP_404_NOT_FOUND)
    

    if comp == request.user.company :
        serializer = CompanySerializer(comp, data = request.data, partial = True)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"message" : "you aren't authrized to do that"}, status=status.HTTP_403_FORBIDDEN)



@api_view(['delete'])
@permission_classes([IsAdmin | IsManager])
def delete_comapny (request, pk) :
    try : 
        company = Company.objects.get(pk = pk)
    except Company.DoesNotExist :
        return Response({
            "error" : "Company not found"
        }, status = status.HTTP_404_NOT_FOUND)
    
    if company == request.user.company :
        company.delete()
        return Response({
            "message" : "Company removed successfully"
        }, status=status.HTTP_200_OK)
    
    return Response({
        "message" : "you aren't autherized to delete this company"
    }, status=status.HTTP_403_FORBIDDEN)


@api_view(['get'])
@permission_classes([IsAdmin])
def get_all_companies (request) :
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True, context={'request' : request})

    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['get'])
@permission_classes([IsAdmin | IsClient])
def get_company_details (request, pk) :
    company = Company.objects.get(pk=pk)
    if company == request.user.company :
        serializer = CompanySerializer(company , context={"request" : request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({
        "message" : "you are unotherized to see that"
    }, status=status.HTTP_200_OK)
    



@api_view(['post'])
@permission_classes([IsAdmin])
def addCategorie (request) : 
    serializer = InsuranceCategorySerializer(data = request.data)

    if serializer.is_valid() :
        category = serializer.save()
        return Response({
            "message" : "new categorie added successfully",
            "category" : InsuranceCategorySerializer(category).data
        }, status=status.HTTP_201_CREATED)
    
    return Response( serializer.errors ,status=status.HTTP_400_BAD_REQUEST)



@api_view(['post'])
@permission_classes([IsAdmin | IsManager])

def inviteManager (request, company_id, manager_id) :
    user = request.user
    if user.company != company_id :
        return Response({
            "error" : "You're not authorized to invite this member"
        }, status=status.HTTP_403_FORBIDDEN)
    
    invite = ManagerInvite.objects.create(company = company_id, manager=manager_id)
    try :
        send_mail(
            f"You are invited to be a manager of {invite.company.name}",
            "The company {invite.company.name} have send you this token to register you as a new manager pleas folow the link below to porced\ntoken : {invite.token}\nconfirmatio page : https://confirm_token.com",
            settings.DEFAULT_FROM_EMAIL,
            invite.manager.email
        )
        return Response({"massege" : "Invite sent"}, status=status.HTTP_200_OK)
    except (BadHeaderError, smtplib.SMTPException) as e :
        return Response({"massege" : "Error while sending the email"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([AllowAny])

def companyProducts (request, company_id) :
    try : 
        company = Company.objects.get(pk=company_id)
    except Company.DoesNotExist :
        return Response({"error" : "Company Doesnt exist"}, status=status.HTTP_404_NOT_FOUND)
    
    products = company.products.all()
    serializer = IPSerializer(products, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def companyContracts (request, company_id) :
    try : 
        company = Company.objects.get(pk=company_id)
    except Company.DoesNotExist :
        return Response({"error" : "Company Doesnt exist"}, status=status.HTTP_404_NOT_FOUND)
    
    products = company.products.all()
    contracts = Contract.objects.filter(product__in =products)

    serializer = ContractSerializer(contracts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)