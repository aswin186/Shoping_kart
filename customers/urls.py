from django.urls import path
from customers import views

urlpatterns = [
    path('account/', views.signup_in, name='signup_in'),
    path('logOut/', views.logout_view, name='logout'),
    path('profile_view', views.profile_view, name='account_details'),
]