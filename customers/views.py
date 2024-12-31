from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile, UserAddress
from django.contrib import messages

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.urls import reverse

from django.contrib.auth import get_user_model
from django.http import HttpResponse

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

            user.is_active = False
            user.save()

            # Email verification link
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            link = request.build_absolute_uri(
                reverse('activate', kwargs={'uidb64': uid, 'token': token})
            )

            subject = 'Activate Your Account'
            send_mail(subject, link, 'from@example.com', [email])

            success_message = "User Successfully Registered login and Update Your Profile Details"
            messages.success(request, success_message)
            return redirect('account_activation_sent')
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


def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('signup_in')
    else:
        return HttpResponse('Activation link is invalid!')