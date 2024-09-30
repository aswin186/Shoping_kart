from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages

def account_details(request):
    context = {}
    if request.POST and 'register' in request.POST:
        context['register'] = True
        try:
            print(request.POST)
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            user = User.objects.create_user(username=username, email=email, password=password)
            userProfile = UserProfile.objects.create(user=user)

            success_message = "User Successfully Registered Update Your Profile Details"
            messages.success(request, success_message)
            return redirect('index')
        except Exception as e:
            error_message = "Username alredy exists"
            messages.error(request, error_message)

    if request.POST and 'login' in request.POST:
        context['register'] = False
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = "Incorrect credentials"
            messages.error(request, error_message)
    return render(request, 'account.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')