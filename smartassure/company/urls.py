from django.urls import path
from .views import *

urlpatterns = [
    path('', get_all_companies, name='allCompanies'),
    path('<int:pk>/', get_company_details, name='getCompany'),
    path('add/', addCompanyView, name='addCompany'),
    path('add/cat/', addCategorie, name='addCategory'),
    path('add/<int:pk>', updateCompanyView, name='updateCompany'),
    path('delete/<int:pk>', delete_comapny, name='deleteCompany'),
]