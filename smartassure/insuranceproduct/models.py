from django.db import models
from company.models import Company, InsuranceCategory

# Create your models here.
class InsuranceProduct (models.Model) :
    name = models.CharField(max_length=255)
    category = models.ManyToManyField(InsuranceCategory, related_name='product_category')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.PositiveIntegerField()
    details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)