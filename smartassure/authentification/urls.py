from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_user_view, name='register'),
    path('login/', user_login_view, name='login'),
    path('logout/', logout, name='logout'),
    path('users/', getuUsers, name='getUsers'),
    path('user/<int:pk>', getUserDetails, name='getUserDetails'),
    path('user/add/<int:pk>', updateUser, name='updateUser'),
]