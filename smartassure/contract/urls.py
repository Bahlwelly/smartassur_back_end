from django.urls import path
from .views import *


urlpatterns = [
    path('', getAllContracts, name='getContracts'),
    path('add/', createContract, name='createContract'),
    path('add/<int:pk>', updateContract, name='updateContract'),
    path('user/<int:user_id>', getUserContracts, name='userContracts'),
    path('company/<int:contract_id>', contractCompany, name='contractComany'),
]