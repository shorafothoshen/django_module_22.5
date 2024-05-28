from django.db import models
from django.contrib.auth.models import User
from .constants import ACCOUTN_TYPE,GENDER_TYPE
# Create your models here.

class BankAccountModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name="account")
    account_type=models.CharField(max_length=20, choices=ACCOUTN_TYPE)
    account_no=models.IntegerField(unique=True)
    birthday=models.DateField(null=True,blank=True)
    gender=models.CharField(max_length=15,choices=GENDER_TYPE)
    initial_deposite_date=models.DateField(auto_now_add=True)
    balance=models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return str(self.account_no)
    
class UserAddressModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name="address")
    street_address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    postal_code=models.IntegerField()
    country=models.CharField(max_length=100)

    def __str__(self):
        return self.user.email

class IsBankrupt(models.Model):
    bankrupt=models.BooleanField(default=False,blank=True,null=True)