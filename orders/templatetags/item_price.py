from django import template
import math

register = template.Library()

@register.simple_tag()
def calc_price(quantity, sub_price):
    single_price = sub_price/quantity
    return float(math.floor(single_price))