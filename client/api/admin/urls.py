from django.urls import path
from . import views


urlpatterns = [ 
    path('customers', views.AllCustomersListApiView.as_view()),
    path('summary/applications', views.LoanApplicationSummaryApiView.as_view()),
    path('summary/loans', views.LoanSummaryApiView.as_view()),
    path('summary/customers', views.CustomerSummaryApiView.as_view()),
    path('customers/<str:uuid>', views.CustomerRetrieveApiView.as_view()),
    path('customers/<str:uuid>/disable', views.CustomerDisableApiView.as_view()),
    path('customers/<str:uuid>/enable', views.CustomerEnableApiView.as_view()), 
    path('customers/<str:uuid>/applications', views.CustomerApplicationListApiView.as_view()),  
    path('customers/<str:uuid>/loans', views.CustomerLoansListApiView.as_view()),   
    path('applications', views.AllLoanApplicationApiView.as_view()),
    path('applications/<str:uuid>', views.ApplicationDetailApiView.as_view()),
    path('loans', views.AllLoanApiView.as_view()),
    path('loans/<str:uuid>', views.LoanDetailApiView.as_view()), 
]