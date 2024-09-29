from django.urls import path
from customers import views

urlpatterns = [
    path('account/', views.account_details, name='account_details'),
]