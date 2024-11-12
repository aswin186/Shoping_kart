from django import template

register = template.Library()

@register.simple_tag()
def get_payment_status(status):
    stage = ['No_Status', 'COD', 'Payed']
    return stage[status]