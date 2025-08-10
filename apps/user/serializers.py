from rest_framework import serializers
from apps.user.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }
        
    def validate_email(self, value):
        if UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

  

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user
    


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = f"{user.id}"
        token['email'] = user.email
        token['superuser'] = user.is_superuser
        token['is_acitve'] = user.is_active
        return token
    
    def validate(self, attrs):
        user = self.context['user']

        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    