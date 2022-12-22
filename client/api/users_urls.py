from django.urls import path
from . import views



urlpatterns = [ 
    path('', views.CustomersListApiView.as_view()),
    path('bankaccount', views.UserBankListApiView.as_view()), 
    path('debitcard', views.UserCardListApiView.as_view()), 
    path('loandebt', views.UserLoanRemainingApiView.as_view()), 
    path('loans', views.UserLoansApiView.as_view()), 
]