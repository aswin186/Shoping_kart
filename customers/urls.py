from django.urls import path
from customers import views

urlpatterns = [
    path('account/', views.signup_in, name='signup_in'),
    path('logOut/', views.logout_view, name='logout'),
    path('profile_view', views.profile_view, name='account_details'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]