from django.db import models

from app.clients.models import Client
from app.products.models import Product


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.client.name} - {self.datetime}'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.order.id} - {self.product.name} - {self.quantity}'
