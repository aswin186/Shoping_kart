from django.shortcuts import render


def cart_details(request):
    return render(request, 'cart_layout.html')