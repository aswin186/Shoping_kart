from django import template
import math

register = template.Library()

@register.simple_tag()
def calc_subTotal(quantity, price, discount):
    dis_price = price - (price * discount)/100
    sub_total = int(quantity) * dis_price
    return float(math.floor(sub_total))
