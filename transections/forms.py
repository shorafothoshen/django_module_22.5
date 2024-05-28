from django import forms
from .models import TransactionModel

class TransactionForm(forms.ModelForm):
    class Meta:
        model=TransactionModel
        fields=["amount","transaction_type"]

    def __init__(self, *args, **kwargs):
        self.account=kwargs.pop("account") # eikhane get user korew value niya aisha jaito
        super().__init__(*args,**kwargs)
        self.fields["transaction_type"].disabled=True # ei field disabled thekbo user theke
        self.fields["transaction_type"].widget=forms.HiddenInput() # ei field hide thekbo user er kase
    def save(self,commit=True):
        self.instance.account=self.account
        self.instance.balance_after_transaction=self.account.balance
        return super().save()
    
class DepositForm(TransactionForm):
    def clean_amount(self): #amount field ke filter krbo
        min_deposit_amount=100
        amount=self.cleaned_data.get("amount") # user er fillup kora form theke amra amount field er value ke niya aslam
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f"You need to deposit at least{min_deposit_amount}"
            )
        
        return amount

class WithdrawalForm(TransactionForm):
    def clean_amount(self):
        account=self.account
        min_withdraw_amount=500
        max_withdraw_amount=20000
        balance=account.balance
        amount=self.cleaned_data.get("amount")

        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f"You can withdraw at least {min_withdraw_amount}"
            )
        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f"You can withdraw at most {max_withdraw_amount}"
            )
        
        if amount> balance:
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )
        
        return amount
    
class LoanForm(TransactionForm):
    def clean_amount(self):
        amount=self.cleaned_data.get("amount")

        return amount
    
class BalanceTransferForm(forms.Form):
    account_no = forms.IntegerField(label="Recipient Account Number")
    amount = forms.DecimalField(max_digits=12, decimal_places=2)