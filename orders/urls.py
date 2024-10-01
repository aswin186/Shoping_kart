from django.urls import path
from orders import views

urlpatterns = [
    path('cart', views.cart_details, name='cart_details'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart <pk>', views.remove_from_cart, name='remove_from_cart'),
    path('conform_order', views.conform_order, name='conform_order'),
    path('track_ordes', views.track_orders, name='track_orders'),
]