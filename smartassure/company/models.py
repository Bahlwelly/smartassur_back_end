from django.db import models
from authentification.models import User

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