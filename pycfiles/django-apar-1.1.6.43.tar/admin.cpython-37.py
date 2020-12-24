# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/vouchers/admin.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1537 bytes
from django.contrib import admin
from aparnik.contrib.basemodels.admin import BaseModelAdmin
from aparnik.contrib.users.admin import get_user_search_fields
from .models import Voucher

class VoucherAdmin(BaseModelAdmin):
    fields = [
     'user_obj', 'quantity', 'order_item_obj', 'expire_at', 'is_active', 'is_spent', 'quantity_remain']
    list_display = ['user_obj', 'quantity', 'is_spent', 'quantity_remain', 'expire_at', 'is_active']
    list_filter = []
    search_fields = get_user_search_fields('user_obj')
    exclude = []
    dynamic_raw_id_fields = []
    inlines = []
    raw_id_fields = ['user_obj', 'order_item_obj']

    def __init__(self, *args, **kwargs):
        Klass = VoucherAdmin
        Klass_parent = BaseModelAdmin
        (super(Klass, self).__init__)(*args, **kwargs)
        self.fields = Klass_parent.fields + self.fields
        self.list_display = Klass_parent.list_display + self.list_display
        self.list_filter = Klass_parent.list_filter + self.list_filter
        self.search_fields = Klass_parent.search_fields + self.search_fields
        self.exclude = Klass_parent.exclude + self.exclude
        self.dynamic_raw_id_fields = Klass_parent.dynamic_raw_id_fields + self.dynamic_raw_id_fields
        self.raw_id_fields = Klass_parent.raw_id_fields + self.raw_id_fields
        self.inlines = Klass_parent.inlines + self.inlines

    class Meta:
        model = Voucher


admin.site.register(Voucher, VoucherAdmin)