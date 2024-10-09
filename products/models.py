from django.db import models

# Create your models here.
class Product(models.Model):

    live = 1
    delete = 0
    product_status = ((live, 'Live'), (delete, 'Delete'))

    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='products/')
    priority = models.IntegerField(default=0)
    delete_status = models.IntegerField(default=live, choices=product_status)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
