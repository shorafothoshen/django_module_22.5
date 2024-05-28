from django.contrib import admin
from .models import TransactionModel
# Register your models here.

@admin.register(TransactionModel)

class TransactionAdmin(admin.ModelAdmin):
    list_display=["amount","balance_after_transaction","transaction_type","loan_approve","timestamp"]

    def save_model(self,request,obj,form,change):
        obj.account.balance+=obj.amount
        obj.balance_after_transaction=obj.account.balance
        obj.account.save()
        return super().save_model(request,obj,form,change)