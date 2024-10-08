from django.db import models
from customers.models import UserProfile
from products.models import Product


# Create your models here.

class Order(models.Model):
    live = 1
    delete = 0
    status = ((live, 'Live'), (delete, 'Delete'))

    cart_stage = 0
    order_confirmed = 1
    order_processing = 2
    order_delivered = 3
    order_rejected = -1
    order_status = ((order_confirmed, 'order_confirmed'),(order_processing, 'order_processing'),
                    (order_delivered, 'order_delivered'),
                    (order_rejected, 'order_rejected'))

    order_stage = models.IntegerField(choices=order_status, default=cart_stage)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name='carts', null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cart_status = models.IntegerField(choices=status, default=live)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='cart_items')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    owner = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='added_items')