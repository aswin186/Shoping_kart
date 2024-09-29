from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    featured_products = Product.objects.order_by('priority')[:4]
    latest_products = Product.objects.order_by('-created_at')[:8]
    context = {'featured_products': featured_products, 'latest_products': latest_products}
    return render(request, 'index.html', context)

def list_products(request):
    all_products = Product.objects.all()
    page = 1
    if request.GET:
        page = request.GET.get('page',1)
    product_paginator = Paginator(all_products, 8)
    all_products = product_paginator.get_page(page)
    context = {'all_products': all_products}
    return render(request, 'products.html', context)

def product_details(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}
    return render(request, 'product_details.html', context)
