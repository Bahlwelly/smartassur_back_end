from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User


User = get_user_model()

class UserRegisterSerializer (serializers.ModelSerializer) :
    password = serializers.CharField(write_only = True , max_length=8)
    password2 = serializers.CharField(write_only = True ,label = 'confirmer le mot de pass', max_length=8)

    class Meta:
        model = User
        fields = ['telephone', 'first_name', 'last_name', 'email', 'role', 'password', 'password2', 'profile']

    
    def validate_password (self, value) :
        try :
            validate_password(value)
        except ValidationError as e :
            raise serializers.ValidationError(e.messages)
        return value
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2'] :
            raise serializers.ValidationError({"password" :"Password confirmation doesn't match the password."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)   
        user.set_password(password)
        user.save()

        return user
    

class UserLoginSerializer (serializers.Serializer) :
    telephone = serializers.IntegerField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        telephone = attrs.get('telephone')
        password = attrs.get('password')

        if telephone and password :
            user = authenticate(request= self.context.get('request'), telephone = telephone, password = password)

            if not user :
                raise serializers.ValidationError(_('invalid phone number or password'))
        
        else :
            raise serializers.ValidationError(_('phone number and password are required'))

        attrs['user'] = user
        return attrs



class UserSerializer (serializers.ModelSerializer) :
    class Meta :
        model = User
        fields = ['first_name', 'last_name', 'email', 'telephone', 'role', 'profile']