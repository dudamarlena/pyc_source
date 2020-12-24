# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plugshop/models/order_products.py
# Compiled at: 2014-08-09 03:47:51
from django.db import models
from django.utils.translation import ugettext_lazy as _
from plugshop import settings
from plugshop.utils import is_default_model

class OrderProductsAbstract(models.Model):

    class Meta:
        abstract = True
        verbose_name = _('order product')
        verbose_name_plural = _('order product')

    quantity = models.PositiveIntegerField(_('quantity'), blank=False, null=False, default=1)
    order = models.ForeignKey(settings.ORDER_MODEL, verbose_name=_('order'), related_name='ordered_items')
    product = models.ForeignKey(settings.PRODUCT_MODEL, verbose_name=_('product'))

    def price(self):
        return self.product.price * self.quantity

    price.short_description = _('Total price')


if is_default_model('ORDER_PRODUCTS'):

    class OrderProducts(OrderProductsAbstract):

        class Meta:
            app_label = 'plugshop'
            verbose_name = _('order product')
            verbose_name_plural = _('order product')