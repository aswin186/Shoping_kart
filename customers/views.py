from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile, UserAddress
from django.contrib import messages

def signup_in(request):
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
            userProfile.save()
            userAddress = UserAddress.objects.create(user=userProfile)
            userAddress.save()

            success_message = "User Successfully Registered login and Update Your Profile Details"
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

    return render(request, 'accounts/account.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')


def profile_view(request):
    user_info = request.user
    customer_info = user_info.user_profile
    customer_address = customer_info.address_profile

    # username = user_info.username
    # name = customer_info.name
    # phone = customer_info.phone
    # email = user_info.email
    # street = models.CharField(max_length=120, null=True)
    # city = models.CharField(max_length=120, null=True)
    # district = models.CharField(max_length=120, null=True)
    # state = models.CharField(max_length=120, null=True)
    # country = models.CharField(max_length=120, null=True)
    # land_mask = models.CharField(max_length=120, null=True)
    # pincode = models.CharField(max_length=120, null=True)

    # context = {'username': username, 'name': name, 'address': address, 'phone': phone, 'email': email}
    context = {'user_info': user_info}

    if request.POST and 'update_profile' in request.POST:
        user_info = request.user
        customer_info = user_info.user_profile
        print(request.POST)

        customer_info.name = request.POST['name']
        customer_info.phone = request.POST['phone']
        user_info.email = request.POST['email']

        customer_info.save()
        user_info.save()

    if request.POST and 'update_address' in request.POST:
        user_info = request.user
        customer_info = user_info.user_profile
        customer_address = customer_info.address_profile
        print(request.POST)

        customer_address.street = request.POST['street']
        customer_address.city = request.POST['city']
        customer_address.district = request.POST['district']
        customer_address.state = request.POST['state']
        customer_address.country = request.POST['country']
        customer_address.pincode = request.POST['pincode']
        customer_address.land_mark = request.POST['landmark']

        customer_address.save()



    return render(request, 'accounts/account.html', context)