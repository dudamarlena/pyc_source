# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Development/customapps/valuehorizon-forex/forex/admin.py
# Compiled at: 2016-06-02 13:23:51
from django.contrib import admin
from forex.models import Currency, CurrencyPrice

class CurrencyAdmin(admin.ModelAdmin):
    search_fields = [
     'name']
    list_display = ('name', 'symbol', 'digits', 'num_code', 'ascii_symbol')


admin.site.register(Currency, CurrencyAdmin)

class CurrencyPriceAdmin(admin.ModelAdmin):
    list_filter = [
     'currency']
    list_display = ('currency', 'date', 'ask_price', 'bid_price')


admin.site.register(CurrencyPrice, CurrencyPriceAdmin)