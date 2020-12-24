# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drmartiner/projects/django-paymecash/paymecash/admin.py
# Compiled at: 2013-09-17 09:37:16
from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'result', 'wallet_id', 'product_price', 'product_currency',
                    'payment_type_group_id', 'transaction_id', 'created')
    list_filter = ('wallet_id', 'payment_type_group_id', 'result', 'created')
    search_fields = ('order_id', 'transaction_id', 'cs1', 'cs2', 'cs3')


admin.site.register(Payment, PaymentAdmin)