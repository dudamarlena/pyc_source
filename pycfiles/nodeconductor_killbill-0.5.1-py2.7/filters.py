# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_killbill/filters.py
# Compiled at: 2016-09-25 09:47:37
import django_filters
from .models import Invoice

class InvoiceFilter(django_filters.FilterSet):
    customer = django_filters.CharFilter(name='customer__uuid', distinct=True)
    customer_name = django_filters.CharFilter(name='customer__name', lookup_type='icontains', distinct=True)
    customer_native_name = django_filters.CharFilter(name='customer__native_name', lookup_type='icontains', distinct=True)
    customer_abbreviation = django_filters.CharFilter(name='customer__abbreviation', lookup_type='icontains', distinct=True)
    month = django_filters.CharFilter(name='date', lookup_type='month')
    year = django_filters.CharFilter(name='date', lookup_type='year')

    class Meta(object):
        model = Invoice
        fields = [
         'customer', 'customer_name', 'customer_native_name', 'customer_abbreviation',
         'year', 'month',
         'amount',
         'date']
        order_by = [
         'date',
         '-date',
         'amount',
         '-amount',
         'customer__name',
         '-customer__name',
         'customer__abbreviation',
         '-customer__abbreviation',
         'customer__native_name',
         '-customer__native_name']
        order_by_mapping = {'customer_name': 'customer__name', 
           'customer_abbreviation': 'customer__abbreviation', 
           'customer_native_name': 'customer__native_name'}