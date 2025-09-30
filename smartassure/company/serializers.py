from rest_framework import serializers
from .models import Company, InsuranceCategory

class InsuranceCategorySerializer (serializers.ModelSerializer) :
    subcats = serializers.SerializerMethodField()

    class Meta :
        model = InsuranceCategory
        fields = ['id', 'name', 'subcats', 'parent']


    def get_subcats (self, obj) :
        return [
            {"id" : sub.id, "name" : sub.name}
            for sub in obj.subcategories.all()
        ]


class CompanySerializer (serializers.ModelSerializer) :
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=InsuranceCategory.objects.all()
    )

    class Meta : 
        model = Company
        fields = '__all__'