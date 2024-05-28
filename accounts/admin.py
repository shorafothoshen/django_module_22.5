from django.contrib import admin
from .models import BankAccountModel,UserAddressModel,IsBankrupt
# Register your models here.

@admin.register(BankAccountModel)
class RegistationAdmin(admin.ModelAdmin):
    list_display=["account_no","account_type","gender","balance","initial_deposite_date"]

@admin.register(UserAddressModel)
class AddressAdmin(admin.ModelAdmin):
    list_display=["street_address","city","country"]

@admin.register(IsBankrupt)
class BankruptAdmin(admin.ModelAdmin):
    list_display=["bankrupt"]

