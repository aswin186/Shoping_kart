from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from orders.templatetags.item_sub_total import calc_subTotal
from django.core.mail import send_mail


def cart_details(request):
    user_info = request.user
    customer = user_info.user_profile

    cart_obj, created = Order.objects.get_or_create(
        user=customer,
        order_stage=Order.cart_stage)

    context = {'cart_obj': cart_obj}

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
            order_stage = Order.cart_stage)

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


def remove_from_cart(request, pk):
    item = OrderItem.objects.get(pk=pk)
    if item:
        item.delete()
    return redirect('cart_details')


def conform_order(request):
    if request.method == 'POST':
        try:
            user_info = request.user
            customer = user_info.user_profile
            total = float(request.POST.get('total'))
            print(total)
            order_obj = Order.objects.get(user=customer, order_stage=Order.cart_stage)

            if order_obj:
                order_obj.order_stage = Order.order_confirmed
                order_obj.total_price = total
                order_obj.save()

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
                    subject=f"Conformation of order from {customer.name}",
                    message=f"order conformed Order ID:- {order_obj.id} "+f"Total price:- {order_obj.total_price} "+f"Products:- {item_name} "+f"Quantity:- {item_quantity} "+f"Sub_total:- {item_sub_price}",
                    from_email=user_info.email,
                    recipient_list=['aswinachu1812@gmail.com', 'aswinns640@gmail.com'],
                )

                status_message = 'Order Confirmed'
                messages.success(request, status_message)
            else:
                status_message = "Order Can't processed"
                messages.error(request, status_message)

        except Exception as e:
            status_message = "Order Can't processed, No items in cart"
            messages.error(request, status_message)

        return redirect('cart_details')



def track_orders(request):
    user_info = request.user
    customer = user_info.user_profile

    all_orders = Order.objects.filter(user=customer).exclude(order_stage=Order.cart_stage).order_by('-created_at')

    context = {'all_orders': all_orders}

    return render(request, 'cart_order/orders_layout.html', context)

def order_detaile(request, pk):

    order_obj = Order.objects.get(pk=pk)
    context = {'order_obj': order_obj}
    return render(request, 'cart_order/order_list.html', context)