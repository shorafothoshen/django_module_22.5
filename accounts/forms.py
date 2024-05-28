from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import BankAccountModel,UserAddressModel
from .constants import GENDER_TYPE,ACCOUTN_TYPE
class RegistationForm(UserCreationForm):
    account_type=forms.ChoiceField(choices=ACCOUTN_TYPE)
    birthday=forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    gender=forms.ChoiceField(choices=GENDER_TYPE)
    street_address=forms.CharField(max_length=100)
    city=forms.CharField(max_length=100)
    postal_code=forms.IntegerField()
    country=forms.CharField(max_length=100)
    class Meta:
        model=User
        fields=["username","first_name","last_name","email","password1","password2","birthday","account_type","gender","street_address","city","postal_code","country"]
    def save(self,commit=True):
        our_user=super().save(commit=False)
        if commit==True:
            our_user.save()
            account_type=self.cleaned_data.get("account_type")
            birthday=self.cleaned_data.get("birthday")
            gender=self.cleaned_data.get("gender")
            street_address=self.cleaned_data.get("street_address")
            postal_code=self.cleaned_data.get("postal_code")
            city=self.cleaned_data.get("city")
            country=self.cleaned_data.get("country")

            BankAccountModel.objects.create(
                user=our_user,
                account_type=account_type,
                birthday=birthday,
                gender=gender,
                account_no=10000 + our_user.id
            )
            UserAddressModel.objects.create(
                user=our_user,
                street_address=street_address,
                postal_code=postal_code,
                city=city,
                country=country,
            )
        return our_user
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class":'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
            })

class UserUpdateForm(forms.ModelForm):
    account_type=forms.ChoiceField(choices=ACCOUTN_TYPE)
    birthday=forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    gender=forms.ChoiceField(choices=GENDER_TYPE)
    street_address=forms.CharField(max_length=100)
    city=forms.CharField(max_length=100)
    postal_code=forms.IntegerField()
    country=forms.CharField(max_length=100)
    class Meta:
        model=User
        fields=["first_name","last_name","email"]
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class":'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
            })
        
        if self.instance:
            try:
                user_account=self.instance.account
                user_address=self.instance.address
            except BankAccountModel.DoesNotExist:
                user_account=None
                user_address=None
            
            if user_account:
                self.fields["account_type"].initial=user_account.account_type
                self.fields["gender"].initial=user_account.gender
                self.fields["birthday"].initial=user_account.birthday
                self.fields["street_address"].initial=user_address.street_address
                self.fields["city"].initial=user_address.city
                self.fields["postal_code"].initial=user_address.postal_code
                self.fields["country"].initial=user_address.country
    
    def save(self, commit=True):
        user=super().save(commit=False)
        if commit:
            user.save()

            user_account, created=BankAccountModel.objects.get_or_create(user=user)
            user_address, created=UserAddressModel.objects.get_or_create(user=user)

            user_account.account_type=self.cleaned_data["account_type"]
            user_account.gender=self.cleaned_data["gender"]
            user_account.birthday=self.cleaned_data["birthday"]
            user_account.save()

            user_address.street_address=self.cleaned_data["street_address"]
            user_address.city=self.cleaned_data["city"]
            user_address.postal_code=self.cleaned_data["postal_code"]
            user_address.country=self.cleaned_data["country"]
            user_address.save()
            
        return user
