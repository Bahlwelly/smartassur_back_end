from rest_framework import serializers
from .models import Contract

class ContractSerializer (serializers.ModelSerializer) :
    client = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta :
        model = Contract
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        return Contract.objects.create(client=user , **validated_data)