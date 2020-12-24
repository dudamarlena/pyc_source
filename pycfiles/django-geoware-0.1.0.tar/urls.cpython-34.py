# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/doozdev/backend/restful-backend/apps/geoware/urls.py
# Compiled at: 2017-01-27 09:53:00
# Size of source mod 2**32: 1177 bytes
from django.conf.urls import url
from dal import autocomplete
from .views import *
urlpatterns = [
 url('^country/autocomplete/$', CountryAutocompleteView.as_view(), name='country-autocomplete'),
 url('^division/autocomplete/$', DivisionAutocompleteView.as_view(), name='division-autocomplete'),
 url('^subdivision/autocomplete/$', SubdivisionAutocompleteView.as_view(), name='subdivision-autocomplete'),
 url('^city/autocomplete/$', CityAutocompleteView.as_view(), name='city-autocomplete'),
 url('^timezone/autocomplete/$', TimezoneAutocompleteView.as_view(), name='timezone-autocomplete'),
 url('^altnames/autocomplete/$', AltnameAutocompleteView.as_view(), name='altnames-autocomplete'),
 url('^currency/autocomplete/$', CurrencyAutocompleteView.as_view(), name='currency-autocomplete'),
 url('^language/autocomplete/$', LanguageAutocompleteView.as_view(), name='language-autocomplete')]