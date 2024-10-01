from django import template
import math

register = template.Library()

@register.simple_tag()
def calc_Total(cart):
    total = 0
    for item in cart.added_items.all():

        print(item.quantity)
        print(item.product.price)
        print(item.product.discount)
        dis_price = item.product.price - (item.product.price * item.product.discount)/100
        sub_total = item.quantity * dis_price
        total += sub_total
    return float(math.floor(total))