from django.urls import path
from .views import *

urlpatterns = [
    path('', get_all_companies, name='allCompanies'),
    path('<int:pk>/', get_company_details, name='getCompany'),
    path('products/<int:company_id>/', companyProducts, name='getCompanyProducts'),
    path('contracts/<int:company_id>/', companyContracts, name='getCompanyContracts'),
    path('add/', addCompanyView, name='addCompany'),
    path('add/cat/', addCategorie, name='addCategory'),
    path('add/<int:pk>', updateCompanyView, name='updateCompany'),
    path('delete/<int:pk>', delete_comapny, name='deleteCompany'),
    path('invite/<int:company_id>/<int:manager_id>', inviteManager, name='inviteManager')
]