# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/imposeren/kava/django-currency/.env/lib/python2.7/site-packages/currency/admin.py
# Compiled at: 2013-10-18 05:53:59
from django.contrib import admin
from .models import Currency, ExchangeRate

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'full_name', 'short_name')


class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('date', 'base_currency', 'foreign_currency', 'rate')
    list_filter = ('date', 'base_currency')


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ExchangeRate, ExchangeRateAdmin)