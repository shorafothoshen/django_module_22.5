
from django.urls import path
from . import views

urlpatterns = [
    path("deposit/", views.DepositMoneyView.as_view(), name="deposit_money"),
    path("withdraw/", views.WithdrawMoneyView.as_view(), name="withdraw_money"),
    path("loan_request/", views.LoanRequestView.as_view(), name="loan_request"),
    path("report/", views.TransactionReportView.as_view(), name="transaction_report"),
    path("loan_list/", views.LoanListView.as_view(), name="Loan_list"),
    path("pay_loan/<int:Loan_id>", views.PayLoanView.as_view(), name="pay_loan"),
    path("transfer/",views.BalanceTransferView.as_view(),name="transfer"),
]
