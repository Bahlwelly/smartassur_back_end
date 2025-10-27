from django.db import models
from authentification.models import User
from insuranceproduct.models import InsuranceProduct
from company.models import Company
from django.utils import timezone
# Create your models here.


class Contract (models.Model) :
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contracts")
    product = models.ForeignKey(InsuranceProduct, on_delete=models.CASCADE, related_name="contracts")
    status = models.CharField(max_length=50, 
                            choices=[
                                ('pending', 'Pending'),
                                ('active', 'Active'),
                                ('expired', 'Expired'),
                                ('canceled', 'Canceled'),
                            ],
                            default='pending'  
                              )
    type = models.CharField(max_length=100, blank=True)
    signed_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)

    def expired (self) :
        return timezone.now() >= self.end_date
    
    def save(self, *args, **kwargs):
        if not self.type and self.product:
            main_category = self.product.category.filter(id__gte=3, id__lte=8).first()
            if main_category:
                self.type = main_category.name
        super().save(*args, **kwargs)