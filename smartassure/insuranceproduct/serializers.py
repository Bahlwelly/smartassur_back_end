from rest_framework import serializers
from .models import InsuranceProduct

class IPSerializer (serializers.ModelSerializer) :
    class Meta :
        model = InsuranceProduct
        fields = '__all__'
        read_only_fields = ['company']