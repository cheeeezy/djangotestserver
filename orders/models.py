from django.contrib.auth.models import User
from django.db import models

from products.models import Product


# Create your models here.


class SalesOrder(models.Model):
    objects = None
    amount = models.IntegerField()
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Product)