from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)



urlpatterns = [ 
    path('', views.AccountApiView.as_view()),
    path('bvn/verification', views.AccountSetupBvnApiView.as_view()),
    path('debit', views.AddDebitCardApiView.as_view()),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('password/reset', views.ResetPasswordRequestEmailApiView.as_view(), name='password_reset_request_email'),
    path('password/<str:token>/<str:slug>/reset', views.SetNewPasswordTokenCheckApi.as_view(), name='password_reset_done'),
    path('password/change', views.ChangePasswordView.as_view(), name='password_change'),
    path('token',views.LoginApiView.as_view(), name='token_obtain_pair'),   
]