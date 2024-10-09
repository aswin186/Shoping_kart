from django.db import models

# Create your models here.

class Banner(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banners/')
    caption = models.TextField()

