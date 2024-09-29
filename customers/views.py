from django.shortcuts import render

def account_details(request):
    return render(request, 'account.html')