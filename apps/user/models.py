# users/models.py
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db import models
from core.models import BaseModel
from .manager import *


class UserModel(AbstractBaseUser,BaseModel,PermissionsMixin):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=14)
    is_staff = models.BooleanField(default=False)
    is_paid_user = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'



    def __str__(self):
        return self.email
    



    class Meta:
        ordering = ["-id"]