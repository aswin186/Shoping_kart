# Generated by Django 5.1.1 on 2024-11-26 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_category_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='available_quantity',
            field=models.IntegerField(default=0),
        ),
    ]
