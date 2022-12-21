from django.urls import path , include
from account.api.views import UserSignupApiView , PhoneApiView , PhoneVerifyApiView



urlpatterns = [ 
    path('account/', include('account.api.urls') ),
    path('signup/', UserSignupApiView.as_view() ),
    path('signup/phone', PhoneApiView.as_view() ),
    path('signup/phone/verify', PhoneVerifyApiView.as_view() ),
    path('loans/', include('client.api.urls')),  
    path('users', include('client.api.users_urls')),  
    path('admin/', include('client.api.admin.urls')),  
    # path()
]      