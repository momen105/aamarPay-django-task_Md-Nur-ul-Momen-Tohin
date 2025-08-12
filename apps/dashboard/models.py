from core.models import BaseModel
from django.db import models
from apps.user.models import *

class FileUpload(BaseModel):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    filename = models.CharField(max_length=500,null=True,blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    word_count = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.filename}"
    


class PaymentTransaction(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100,unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, null=True,blank=True, choices=[('success', 'Success'), ('failed', 'Failed'),('cancelled', 'Cancelled')])
    currency = models.CharField(max_length=10,null=True,blank=True)
    description = models.TextField( null=True,blank=True)
    customer_name = models.CharField(max_length=100,null=True,blank=True)
    customer_email = models.EmailField(null=True,blank=True)
    customer_phone = models.CharField(max_length=20,null=True,blank=True)
    gateway_response = models.JSONField()

    def __str__(self):
        return self.transaction_id


class ActivityLog(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    metadata = models.JSONField()


    def __str__(self):
        return f"{self.user.username} - {self.action}"