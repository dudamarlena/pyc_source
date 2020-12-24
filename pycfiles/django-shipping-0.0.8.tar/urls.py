# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/marcel/projects/quatix/django-shipping/shipping/urls.py
# Compiled at: 2013-03-16 10:59:36
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('shipping.views', url('countries.json$', 'countries', name='shipping-countries'), url('countries/(?P<country_code>.+)\\.json$', 'states', name='shipping-states'), url('estimation/?$', 'estimation', name='shipping-estimation'))