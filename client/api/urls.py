from django.urls import path
from . import views



urlpatterns = [ 
    path('', views.UserLoanListApiView.as_view()), 
    path('<str:uuid>/schedule', views.LoanScheduleListApiView.as_view()), 
    path('active', views.OutStandingLoanListApiView.as_view()),
    path('applications', views.LoanApplicationRetrieveCreateApiView.as_view()), 
    path('applications/<str:uuid>', views.LoanApplicationRetrieveCreateApiView.as_view()),
    path('loanoffer/accept', views.OfferReceiveApproved.as_view()), 
    path('<str:uuid>', views.LoanRetrieveRequestApiView.as_view()), 
]