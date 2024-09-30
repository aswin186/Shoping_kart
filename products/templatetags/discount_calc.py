from django import template
import math

register = template.Library()

@register.simple_tag()
def calc_discount(price, discount):
    if discount is None or discount <= 0:
        return price
    sell_price = price - (price * discount / 100)
    return float(math.floor(sell_price))