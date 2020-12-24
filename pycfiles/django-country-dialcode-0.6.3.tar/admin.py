# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/areski/projects/django/django-country-dialcode/country_dialcode/admin.py
# Compiled at: 2015-03-11 17:51:58
from django.contrib import admin
from country_dialcode.models import Country, Prefix

class CountryAdmin(admin.ModelAdmin):
    list_display = ('countrycode', 'iso2', 'countryprefix', 'countryname')
    search_fields = ('countryname', 'countryprefix')
    ordering = ('id', )
    list_filter = ['countryprefix', 'countrycode']

    def __init__(self, *args, **kwargs):
        super(CountryAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ('countrycode', )


admin.site.register(Country, CountryAdmin)

class PrefixAdmin(admin.ModelAdmin):
    search_fields = ('prefix', 'destination')
    list_display = ('prefix', 'destination', 'country_name', 'carrier_name')
    ordering = ('prefix', )

    def __init__(self, *args, **kwargs):
        super(PrefixAdmin, self).__init__(*args, **kwargs)


admin.site.register(Prefix, PrefixAdmin)