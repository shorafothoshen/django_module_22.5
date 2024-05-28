from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect,render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import CreateView,ListView
from transections.constants import DEPOSIT, WITHDRAWAL,LOAN, LOAN_PAID,TRANSFER,RECEIVE
from datetime import datetime
from django.urls import reverse_lazy
from django.views import View
from django.db.models import Sum
from .forms import DepositForm,WithdrawalForm,LoanForm,BalanceTransferForm
from .models import TransactionModel
from accounts.models import BankAccountModel,IsBankrupt
# Create your views here.

class TransactionsMoneyView(LoginRequiredMixin,CreateView):
    template_name="transaction/transaction_form.html"
    model=TransactionModel
    title=""
    success_url=reverse_lazy("transaction_report")

    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs.update({
            "account":self.request.user.account
        })

        return kwargs
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
            "title":self.title
        })

        return context
    
class DepositMoneyView(TransactionsMoneyView):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount 
        account.save(
            update_fields=[
                'balance'
            ]
        )
        messages.success(self.request, f"{amount} $ was deposited to your account succussfully")
        return super().form_valid(form)
    
class WithdrawMoneyView(TransactionsMoneyView):
    form_class = WithdrawalForm
    title = 'Withdraw Money'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial

    def form_valid(self, form):
        if IsBankrupt.objects.filter(bankrupt=True).exists():
            messages.success(self.request, "You Bank is Bankrupt You can not Withdraw")
            return redirect("transaction_report")
        else:
            amount = form.cleaned_data.get('amount')
            account = self.request.user.account
            account.balance -= amount 
            account.save(
                update_fields=[
                    'balance'
                ]
            )
            messages.success(self.request, f"Successfully Withdrawn {amount} $ from your account.")
        return super().form_valid(form)
    
class LoanRequestView(TransactionsMoneyView):
    form_class = LoanForm
    title = 'Request For Loan'

    def get_initial(self):
        initial = {'transaction_type': LOAN}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        current_loan_count=TransactionModel.objects.filter(account=self.request.user.account, transaction_type=LOAN, loan_approve= True).count()

        if current_loan_count>=3:
            return HttpResponse("You Have Crossed the Limits")
        messages.success(self.request, f"Loan Request for amount {amount} $ has been successfully sent to admin.")
        return super().form_valid(form)
    
class TransactionReportView(LoginRequiredMixin,ListView):
    template_name="transaction/transaction_report.html"
    model=TransactionModel
    balance=0

    def get_queryset(self):
        queryset=super().get_queryset().filter(
            account=self.request.user.account
        )

        start_date_str=self.request.GET.get("start_date")
        end_date_str=self.request.GET.get("end_date")

        if start_date_str and end_date_str:
            start_date=datetime.strptime(start_date_str,"%Y-%m-%d").date()
            end_date=datetime.strptime(end_date_str,"%Y-%m-%d").date()

            queryset=queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance=TransactionModel.objects.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date).aggregate(Sum("amount"))["amount__sum"]
        else:
            self.balance=self.request.user.account.balance

        return queryset.distinct()
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
            "account":self.request.user.account
        })

        return context

class PayLoanView(LoginRequiredMixin,View):
    def get(self,request,Loan_id):
        Loan=get_object_or_404(TransactionModel,id=Loan_id)
        if Loan.loan_approve:
            user_account=Loan.account
            if Loan.amount<user_account.balance:
                user_account.balance-=Loan.amount
                Loan.balance_after_transaction=user_account.balance
                user_account.save()
                Loan.transaction_type=LOAN_PAID
                Loan.save()
                return redirect("Loan_list")
            else:
                messages.error(self.request, f"Loan amount is greater then available balance")
                return redirect("Loan_list")

class LoanListView(LoginRequiredMixin, ListView):
    model=TransactionModel
    template_name="transaction/loan_request.html"
    context_object_name="Loans"

    def get_queryset(self):
        user_account=self.request.user.account
        queryset=TransactionModel.objects.filter(account=user_account, transaction_type=LOAN)
        return queryset
    
class BalanceTransferView(LoginRequiredMixin,View):
    template_name="transaction/transferMoney.html"

    def get(self,request):
        form=BalanceTransferForm()
        return render(self.request, self.template_name,{"form":form,"title":"Transfer Balance"})
    
    def post(self,request):
        form=BalanceTransferForm(request.POST)
        if form.is_valid():
            from_account=request.user.account
            to_account=form.cleaned_data.get("account_no")
            amount=form.cleaned_data.get("amount")
            try:
                sending_user=BankAccountModel.objects.get(account_no=to_account)
                if from_account!=sending_user:
                    if from_account.balance > amount:
                        from_account.balance-=amount
                        from_account.save()
                        sending_user.balance+=amount
                        sending_user.save()
                        messages.success(request,"Successfully Transfer Balance ✅")
                        TransactionModel.objects.create(
                            account=from_account,
                            amount=amount,
                            balance_after_transaction=from_account.balance,
                            transaction_type=TRANSFER,
                        )
                        TransactionModel.objects.create(
                            account=sending_user,
                            amount=amount,
                            balance_after_transaction=sending_user.balance,
                            transaction_type=RECEIVE
                        )
                    else:
                        messages.error(request,"Not enough money in your account ❌")
                    return redirect("transaction_report")
                else:
                    messages.error(request,"You cannot transfer to your own account ❌")
            except BankAccountModel.DoesNotExist:
                messages.error(request,"❌Not a valid Account Number, Please check the Number and Try again.")
        return render(request,self.template_name,{"form":form,"title":"Transfer Balance"})
