from django.db import models
from customers.models import UserProfile
from products.models import Product


# Create your models here.

class Order(models.Model):
    LIVE = 1
    DELETE = 0
    status = ((LIVE, 'Live'), (DELETE, 'Delete'))

    CART_STAGE = 0
    ORDER_CONFIRMED = 1
    ORDER_PROCESSING = 2
    ORDER_DELIVERED = 3
    ORDER_CANCEL_REQUESTED = 4
    ORDER_CANCELED = -1
    order_status = ((ORDER_CONFIRMED, 'order_confirmed'),(ORDER_PROCESSING, 'order_processing'),
                    (ORDER_DELIVERED, 'order_delivered'), (ORDER_CANCEL_REQUESTED, 'order_cancel_requested'),
                    (ORDER_CANCELED, 'order_canceled'))

    COD = 1
    PAY_NOW = 2
    pay_mode = ((PAY_NOW, 'pay_now'), (COD, 'cod'))

    order_stage = models.IntegerField(choices=order_status, default=CART_STAGE)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name='carts', null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pay_status = models.IntegerField(choices=pay_mode, default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cart_status = models.IntegerField(choices=status, default=LIVE)

    def __str__(self):
        return str(self.id) + "----" + str(self.pay_status)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='cart_items')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    owner = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='added_items')