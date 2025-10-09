from django.db import models
from authentification.models import User
import uuid
from django.utils import timezone
from datetime import timedelta
# Create your models here.
class InsuranceCategory (models.Model) :
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', null=True)


    def __str__(self):
        return self.name


class Company (models.Model) :
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    description = models.TextField()
    website = models.URLField(blank=True)
    email = models.EmailField() 
    phone = models.CharField(max_length=8)
    location = models.CharField(max_length=255, blank=True)
    categories = models.ManyToManyField(InsuranceCategory, related_name='companies_categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

    
def expires_date () :
    return lambda : timezone.now() + timedelta(days=3)

class ManagerInvite (models.Model) :
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=expires_date)
    used = models.BooleanField(default=False)

    def is_valid (self) :
        return not self.used and self.expires_at > timezone.now()