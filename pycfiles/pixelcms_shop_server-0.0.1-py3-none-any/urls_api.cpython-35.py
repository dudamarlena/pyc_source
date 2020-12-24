# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/urls_api.py
# Compiled at: 2016-12-31 06:20:37
# Size of source mod 2**32: 493 bytes
from django.conf.urls import url, include
from shop.catalog import urls_api as catalog_urls_api
from shop.sale import urls_api as sale_urls_api
from shop.payments import urls_api as payments_urls_api
urlpatterns = [
 url('^catalog/', include(catalog_urls_api, namespace='catalog')),
 url('^sale/', include(sale_urls_api, namespace='sale')),
 url('^payments/', include(payments_urls_api, namespace='payments'))]