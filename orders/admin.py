from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_stage', 'total_price', 'updated_at')
    list_filter = ('user', 'order_stage')
    search_fields = ("user__name", "order_stage")

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)