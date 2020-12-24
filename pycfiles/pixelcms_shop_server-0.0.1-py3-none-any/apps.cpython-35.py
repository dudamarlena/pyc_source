# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/apps.py
# Compiled at: 2016-11-23 13:47:02
# Size of source mod 2**32: 168 bytes
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class ShopConfig(AppConfig):
    name = 'shop'
    verbose_name = _('Shop')