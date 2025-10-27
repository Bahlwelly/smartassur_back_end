from django.urls import path
from .views import *

urlpatterns = [
    path('', getAllIPs, name='getIPs'),
    path('<int:pk>/', getIPDetails, name='getIP'),
    path('add/', createIP, name='createIP'),
    path('add/<int:pk>', updateIP, name='updateIP'),
    path('delete/<int:pk>', deleteIP, name='delelteIP'),
    path('company/<int:product_id>', getIPCompany, name='IPCompany')
]