from django.db import models
from company.models import Company, InsuranceCategory

# Create your models here.
class InsuranceProduct (models.Model) :
    lang_original = models.CharField(max_length=5, default='en')
    name_ar = models.CharField(max_length=255, null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    name_fr = models.CharField(max_length=255, null=True, blank=True)
    name_original = models.CharField(max_length=255)
    category = models.ManyToManyField(InsuranceCategory, related_name='product_category')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
    description_ar = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)
    description_fr = models.TextField(null=True, blank=True)
    description_original = models.TextField()
    price = models.PositiveIntegerField()
    details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
