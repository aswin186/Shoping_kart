from django import template

register = template.Library()

@register.simple_tag()
def get_order_status(status):
    # cart_stage = 0
    # order_confirmed = 1
    # order_processing = 2
    # order_delivered = 3
    # order_rejected = -1

    stage = ['Cart', 'Order Processing', 'Order Packing', 'Order Delivered', 'Order Cancel Requested', 'Order Canceled']
    return stage[status]
