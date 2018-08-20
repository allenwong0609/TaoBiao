from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=15)
    price = models.PositiveIntegerField(default=0)
    product_description = models.TextField(default='暂无介绍')
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product_name


class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    photo_description = models.CharField(max_length=20, default='商品照片')
    url = models.URLField(default='http://i.imgur.com/Z230eeq.png')

    def __str__(self):
        return self.photo_description



