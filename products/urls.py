from django.urls import path
from products import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products',views.list_products, name='list_products'),
    path('product_detail <pk>', views.product_details, name='product_details'),
]
