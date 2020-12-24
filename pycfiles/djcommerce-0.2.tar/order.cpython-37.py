# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\jeff\Desktop\CodingDojoPractice\CodingDojoWork\python_stack\django\Django_Commerce\django_commerce\djcommerce\models\order.py
# Compiled at: 2019-06-27 16:29:45
# Size of source mod 2**32: 817 bytes
from django.db import models
from django_extensions.db.models import TimeStampedModel
from .product import ProductInCart
STATUSES = [
 ('cancelled', 'Cancelled'),
 ('complete', 'Complete'),
 ('originated', 'Originated'),
 ('pending', 'Pending'),
 ('shipped', 'Shipped')]

class OrderManager(models.Manager):

    def total_revenue(self, status='Complete'):
        orders = self.filter(status=status)
        return sum([o.get_subtotal() for o in orders])


class Order(TimeStampedModel):
    products = models.ManyToManyField(ProductInCart)
    status = models.CharField(max_length=50, choices=STATUSES)
    objects = OrderManager()

    def get_subtotal(self):
        return sum([p.get_subtotal for p in self.products])

    class Meta:
        abstract = True