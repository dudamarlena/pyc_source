# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plugshop/models/product.py
# Compiled at: 2014-08-09 03:47:51
from django.db import models
from django.utils.translation import ugettext_lazy as _
from plugshop import settings
from plugshop.utils import is_default_model, get_categories
from mptt.fields import TreeForeignKey

class ProductAbstract(models.Model):
    category = TreeForeignKey(settings.CATEGORY_MODEL, blank=True, null=True, verbose_name=_('category'), related_name='products')
    name = models.CharField(_('name'), blank=False, max_length=200)
    slug = models.SlugField(_('slug'), blank=False, unique=True)
    price = models.PositiveIntegerField(_('price'), blank=False)

    class Meta:
        abstract = True
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        categories = get_categories()
        try:
            category = filter(lambda x: x.pk == self.category_id, categories)[0]
            category_path = category.get_path()
        except IndexError:
            category_path = '-'

        return ('plugshop-product', None,
         {'category_path': category_path, 
            'slug': self.slug})


if is_default_model('PRODUCT'):

    class Product(ProductAbstract):

        class Meta:
            app_label = 'plugshop'
            verbose_name = _('product')
            verbose_name_plural = _('products')