from django.urls import path
from . import views



urlpatterns = [ 
    path('', views.CustomersListApiView.as_view()),
]