# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plugshop/admin.py
# Compiled at: 2014-08-09 03:47:51
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from mptt.admin import MPTTModelAdmin
from plugshop import settings
from plugshop.models import *
from plugshop.utils import is_default_model, get_model

class BaseProductAdmin(admin.ModelAdmin):
    inlines = ()
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', 'slug', 'price')
    list_filter = ('category', )

    def changelist_view(self, request, extra_context=None):
        ctx = {}
        return super(BaseProductAdmin, self).changelist_view(request, extra_context=ctx)


if is_default_model('PRODUCT'):
    admin.site.register(get_model(settings.PRODUCT_MODEL), BaseProductAdmin)

class BaseCategoryAdmin(MPTTModelAdmin):
    change_list_template = 'admin/category/change_list.html'
    mptt_level_indent = 20
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', 'get_products', 'slug')

    def get_products(self, instance):
        return ('<br/>').join(p.name for p in instance.products.all())

    get_products.allow_tags = True
    get_products.short_description = _('products')


if is_default_model('CATEGORY'):
    admin.site.register(get_model(settings.CATEGORY_MODEL), BaseCategoryAdmin)

class BaseOrderProductsInline(admin.TabularInline):
    model = get_model(settings.ORDER_PRODUCTS_MODEL)
    extra = 0


class BaseOrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    inlines = (
     BaseOrderProductsInline,)
    search_fields = ('number', 'user')
    list_display = ('number', 'user', 'status', 'price_total', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')


if is_default_model('ORDER'):
    admin.site.register(get_model(settings.ORDER_MODEL), BaseOrderAdmin)