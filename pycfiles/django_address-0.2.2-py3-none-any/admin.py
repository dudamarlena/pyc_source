# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertbanagale/code/opensource/django-address/django-address/example_site/address/admin.py
# Compiled at: 2020-05-10 01:24:31
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from address.models import *

class UnidentifiedListFilter(SimpleListFilter):
    title = 'unidentified'
    parameter_name = 'unidentified'

    def lookups(self, request, model_admin):
        return (('unidentified', 'unidentified'), )

    def queryset(self, request, queryset):
        if self.value() == 'unidentified':
            return queryset.filter(locality=None)
        else:
            return


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ('name', 'code')


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    search_fields = ('name', 'code')


@admin.register(Locality)
class LocalityAdmin(admin.ModelAdmin):
    search_fields = ('name', 'postal_code')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_filter = (UnidentifiedListFilter,)