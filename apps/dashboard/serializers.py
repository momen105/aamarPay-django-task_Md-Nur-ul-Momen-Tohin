from rest_framework import serializers
from .models import *

class FileUploadSerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    
    class Meta:
        model = FileUpload
        fields = '__all__'

    def get_created_date(self, obj):
        if obj.created_at:
            return obj.created_at.date().isoformat() 
        return None

    def get_created_time(self, obj):
        if obj.created_at:
            return obj.created_at.strftime("%I:%M %p")  
        return None

class PaymentTransactionSerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = PaymentTransaction
        fields = '__all__'

    def get_created_date(self, obj):
        if obj.created_at:
            return obj.created_at.date().isoformat() 
        return None

    def get_created_time(self, obj):
        if obj.created_at:
            return obj.created_at.strftime("%I:%M %p")  
        return None

class ActivityLogSerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    class Meta:
        model = ActivityLog
        fields = '__all__'


    def get_created_date(self, obj):
        if obj.created_at:
            return obj.created_at.date().isoformat() 
        return None

    def get_created_time(self, obj):
        if obj.created_at:
            return obj.created_at.strftime("%I:%M %p")  
        return None