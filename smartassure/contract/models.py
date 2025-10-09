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
    signed_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)

    def expired (self) :
        return timezone.now() >= self.end_date
    