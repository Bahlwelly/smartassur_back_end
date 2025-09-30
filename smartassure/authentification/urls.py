from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_user_view, name='register'),
    path('login/', user_login_view, name='login'),
]