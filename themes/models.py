from django.db import models

# Create your models here.

class Banner(models.Model):
    live = 1
    delete = 0
    status = ((live, 'Live'), (delete, 'Delete'))

    not_specified = 0
    home_banner = 1
    product_banner = 2
    cart_banner = 3
    order_banner = 4
    banner_choice = ((not_specified, 'Not Specified'),(home_banner, 'Home Banner'),(product_banner, 'Product Banner'),(cart_banner, 'Cart Banner'),(order_banner, 'Order Banner'))

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banners/')
    caption = models.TextField()
    banner_status = models.IntegerField(choices=status, default=live)
    banner_position = models.IntegerField(choices=banner_choice, default=not_specified)

