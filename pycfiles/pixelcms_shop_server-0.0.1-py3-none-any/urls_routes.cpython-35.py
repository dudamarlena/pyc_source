# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/urls_routes.py
# Compiled at: 2016-12-31 06:20:51
# Size of source mod 2**32: 345 bytes
from django.conf.urls import url, include
from shop.catalog import urls_routes as catalog_urls_routes
from shop.sale import urls_routes as sale_urls_routes
urlpatterns = [
 url('^', include(catalog_urls_routes, namespace='catalog')),
 url('^', include(sale_urls_routes, namespace='sale'))]