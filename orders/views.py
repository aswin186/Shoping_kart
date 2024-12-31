from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from themes.models import Banner
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from orders.templatetags.item_sub_total import calc_subTotal
from django.core.mail import send_mail
from django.core.paginator import Paginator

@login_required(login_url='signup_in')
def cart_details(request):
    cart_banner = Banner.objects.filter(banner_status=Banner.live, banner_position=Banner.cart_banner)
    user_info = request.user
    customer = user_info.user_profile

    cart_obj, created = Order.objects.get_or_create(
        user=customer,
        order_stage=Order.CART_STAGE)

    context = {'cart_obj': cart_obj, 'cart_banner': cart_banner}

    return render(request, 'cart_order/cart_layout.html', context)


@login_required(login_url='signup_in')
def add_to_cart(request):
    if request.method == 'POST':
        user_info = request.user
        customer = user_info.user_profile
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        cart_obj, created = Order.objects.get_or_create(
            user = customer,
            order_stage = Order.CART_STAGE)

        product_obj = Product.objects.get(id=product_id)
        ordered_item, item_created = OrderItem.objects.get_or_create(
            product = product_obj,
            owner = cart_obj)

        if item_created:
            ordered_item.quantity = quantity
            sub_total = calc_subTotal(quantity, product_obj.price, product_obj.discount)
            print(sub_total)
            ordered_item.price = sub_total
            ordered_item.save()
        else:
            ordered_item.quantity = ordered_item.quantity + int(quantity)
            ordered_item.price = int(ordered_item.price) + int(calc_subTotal(quantity, product_obj.price, product_obj.discount))
            ordered_item.save()
        return redirect('cart_details')


@login_required(login_url='signup_in')
def remove_from_cart(request, pk):
    item = OrderItem.objects.get(pk=pk)
    if item:
        item.delete()
    return redirect('cart_details')


@login_required(login_url='signup_in')
def conform_order(request):
    if request.method == 'POST':
        try:
            user_info = request.user
            customer = user_info.user_profile
            total = float(request.POST.get('total'))
            pay_status = request.POST.get('paymentMethod')
            print(pay_status)
            print(total)
            order_obj = Order.objects.get(user=customer, order_stage=Order.CART_STAGE)

            # if order_obj and pay_status == 'PAY_NOW':
            #     order_obj.order_stage = Order.ORDER_CONFIRMED
            #     order_obj.total_price = total
            #     order_obj.pay_status = Order.PAY_NOW
            #     order_obj.save()
            #
            #     item_name = []
            #     item_sub_price = []
            #     item_quantity = []
            #
            #     items = order_obj.added_items.all()
            #     for item in items:
            #         item_name.append(item.product.title)
            #         item_sub_price.append(int(item.price))
            #         item_quantity.append(item.quantity)
            #
            #     print(item_name, item_sub_price, item_quantity)
            #
            #     send_mail(
            #         subject=f"Conformation of order from {customer.name}",
            #         message=f"order conformed Order ID:- {order_obj.id} "+f"Total price:- {order_obj.total_price} "+f"Products:- {item_name} "+f"Quantity:- {item_quantity} "+f"Sub_total:- {item_sub_price}",
            #         from_email=user_info.email,
            #         recipient_list=['aswinachu1812@gmail.com', 'aswinns640@gmail.com'],
            #     )
            #
            #     status_message = 'Order Confirmed'
            #     messages.success(request, status_message)

            if order_obj and pay_status == 'COD':
                order_obj.order_stage = Order.ORDER_CONFIRMED
                order_obj.total_price = total
                order_obj.pay_status = Order.COD
                order_obj.save()

                item_name = []
                item_sub_price = []
                item_quantity = []

                items = order_obj.added_items.all()
                for item in items:
                    item_name.append(item.product.title)
                    item_sub_price.append(int(item.price))
                    item_quantity.append(item.quantity)
                    product_obj = Product.objects.get(id=item.product.id)
                    product_obj.available_quantity = product_obj.available_quantity - item.quantity
                    product_obj.save()

                print(item_name, item_sub_price, item_quantity)

                send_mail(
                    subject=f"Conformation of order from {customer.name}",
                    message=f"order conformed Order ID:- {order_obj.id} "+f"Total price:- {order_obj.total_price} "+f"Products:- {item_name} "+f"Quantity:- {item_quantity} "+f"Sub_total:- {item_sub_price}",
                    from_email=user_info.email,
                    recipient_list=['aswinachu1812@gmail.com', 'aswinns640@gmail.com'],
                )

                status_message = 'Order Confirmed With Cod'
                messages.success(request, status_message)
            else:
                status_message = "Order Can't processed"
                messages.error(request, status_message)

        except Exception as e:
            status_message = "Order Can't processed, No items in cart"
            messages.error(request, status_message)

        return redirect('cart_details')


@login_required(login_url='signup_in')
def track_orders(request):
    order_banner = Banner.objects.filter(banner_status=Banner.live, banner_position=Banner.order_banner)

    user_info = request.user
    customer = user_info.user_profile

    all_orders = Order.objects.filter(user=customer).exclude(order_stage=Order.CART_STAGE).order_by('-created_at')

    page = 1
    if request.GET:
        page = request.GET.get('page', 1)
    order_paginator = Paginator(all_orders, 5)
    all_orders = order_paginator.get_page(page)

    context = {'all_orders': all_orders, 'order_banner': order_banner}

    return render(request, 'cart_order/orders_layout.html', context)


@login_required(login_url='signup_in')
def order_detaile(request, pk):

    order_obj = Order.objects.get(pk=pk)
    context = {'order_obj': order_obj}
    return render(request, 'cart_order/order_content.html', context)


@login_required(login_url='signup_in')
def order_cancel(request, pk):
    order_obj = Order.objects.get(pk=pk)
    order_obj.order_stage = Order.ORDER_CANCEL_REQUESTED
    order_obj.save()

    # Order cancelation request mail
    user_info = request.user
    customer = user_info.user_profile
    mail_id = user_info.email
    item_name = []
    item_sub_price = []
    item_quantity = []

    items = order_obj.added_items.all()
    for item in items:
        item_name.append(item.product.title)
        item_sub_price.append(int(item.price))
        item_quantity.append(item.quantity)

    print(item_name, item_sub_price, item_quantity)
    send_mail(
        subject=f"Cancelation request for order from {customer.name}",
        message=f"Cancelation request for Order ID:- {order_obj.id} " + f"Total price:- {order_obj.total_price} " + f"Products:- {item_name} " + f"Quantity:- {item_quantity} " + f"Sub_total:- {item_sub_price}" + f"Order Cancelation Request Submited, You will receive an order cancelation confirmation email once it accepted",
        from_email=user_info.email,
        recipient_list=['aswinachu1812@gmail.com', 'aswinns640@gmail.com', mail_id],
    )

    status_message = 'Order Cancelation Request Submited, You will receive an order cancelation confirmation email once it accepted'
    messages.success(request, status_message)

    return redirect('order_details', order_obj.id)


@login_required(login_url='signup_in')
def confirm_order_with_paypal(request):
    print("In paypal..............Payment....!")
    if request.method == 'POST':
        try:
            user_info = request.user
            customer = user_info.user_profile
            total = float(request.POST.get('total'))
            pay_status = request.POST.get('pay_status')
            print(pay_status)
            print(total)
            order_obj = Order.objects.get(user=customer, order_stage=Order.CART_STAGE)

            if order_obj and pay_status == 'PAY_NOW':
                order_obj.order_stage = Order.ORDER_CONFIRMED
                order_obj.total_price = total
                order_obj.pay_status = Order.PAY_NOW
                order_obj.save()

                item_name = []
                item_sub_price = []
                item_quantity = []

                items = order_obj.added_items.all()
                for item in items:
                    item_name.append(item.product.title)
                    item_sub_price.append(int(item.price))
                    item_quantity.append(item.quantity)
                    product_obj = Product.objects.get(id=item.product.id)
                    product_obj.available_quantity = product_obj.available_quantity - item.quantity
                    product_obj.save()

                print(item_name, item_sub_price, item_quantity)

                send_mail(
                    subject=f"Conformation of order from {customer.name}",
                    message=f"order conformed Order ID:- {order_obj.id} "+f"Total price:- {order_obj.total_price} "+f"Products:- {item_name} "+f"Quantity:- {item_quantity} "+f"Sub_total:- {item_sub_price}",
                    from_email=user_info.email,
                    recipient_list=['aswinachu1812@gmail.com', 'aswinns640@gmail.com'],
                )

                status_message = 'Order Confirmed with paypal'
                messages.success(request, status_message)
            else:
                status_message = "Order Can't processed"
                messages.error(request, status_message)

        except Exception as e:
            status_message = "Order Can't processed, No items in cart"
            messages.error(request, status_message)

        return redirect('cart_details')