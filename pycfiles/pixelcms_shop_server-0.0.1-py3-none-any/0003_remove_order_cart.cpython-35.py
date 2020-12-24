# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/migrations/0003_remove_order_cart.py
# Compiled at: 2016-12-30 12:22:13
# Size of source mod 2**32: 387 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('shop', '0002_auto_20161230_1608')]
    operations = [
     migrations.RemoveField(model_name='order', name='cart')]