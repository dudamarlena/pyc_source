# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\jeff\Desktop\CodingDojoPractice\CodingDojoWork\python_stack\django\Django_Commerce\django_commerce\djcommerce\models\cart.py
# Compiled at: 2019-06-27 23:16:34
# Size of source mod 2**32: 581 bytes
from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel
from djcommerce.utils import get_product_model
Product = get_product_model()

class Cart(TimeStampedModel):
    products_in_cart = models.ManyToManyField(Product)

    def get_subtotal(self):
        subtotal = 0
        for p in self.products_in_cart.all():
            subtotal += p.get_subtotal()

        return subtotal

    class Meta:
        abstract = False
        if hasattr(settings, 'CART_MODEL'):
            abstract = True