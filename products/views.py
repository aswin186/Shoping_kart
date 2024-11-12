from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from themes.models import Banner
from .models import Product, Category
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    featured_products = Product.objects.order_by('priority')[:4]
    latest_products = Product.objects.order_by('-created_at')[:8]
    home_banner = Banner.objects.filter(banner_status = Banner.home_banner,banner_position= Banner.live)
    context = {'featured_products': featured_products, 'latest_products': latest_products, 'home_banner': home_banner}
    return render(request, 'home/index.html', context)

def list_products(request):
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    product_banner = Banner.objects.filter(banner_status=Banner.live, banner_position=Banner.product_banner)
    page = 1
    if request.GET:
        page = request.GET.get('page',1)
    product_paginator = Paginator(all_products, 8)
    all_products = product_paginator.get_page(page)
    context = {'all_products': all_products, 'product_banner': product_banner, 'all_categories': all_categories}
    return render(request, 'products/products.html', context)

def product_details(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}
    return render(request, 'products/product_details.html', context)


def search_list(request):
    products = Product.objects.all().values_list('title', flat=True)
    product_list = list(products)
    print(product_list)
    return JsonResponse(product_list, safe=False)

def search_product(request):
    if request.method == "POST":
        title = request.POST.get('title')

        if title == "":
            messages.error(request, "Enter product to search")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(title__contains=title).first()

            if product:
                return redirect('product_details', product.id)
            else:
                messages.error(request, "No products mached...")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


def filter_category(request):
    print("Applying filter.................")
    if request.method == "POST":
        category = request.POST.get('filter')
        print(category)
        if category != "" and category != "All":
            cat = Category.objects.filter(name__contains=category).first()
            category_name = cat.name
            all_products = Product.objects.filter(category=cat.id)
            all_categories = Category.objects.all()
            product_banner = Banner.objects.filter(banner_status=Banner.live, banner_position=Banner.product_banner)
            page = 1
            if request.GET:
                page = request.GET.get('page', 1)
            product_paginator = Paginator(all_products, 8)
            all_products = product_paginator.get_page(page)
            context = {'all_products': all_products, 'product_banner': product_banner,
                       'all_categories': all_categories, 'category_name': category_name}
            return render(request, 'products/products.html', context)
        else:
            return redirect('list_products')
    return redirect(request.META.get('HTTP_REFERER'))