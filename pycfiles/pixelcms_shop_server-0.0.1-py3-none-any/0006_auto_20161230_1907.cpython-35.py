# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/migrations/0006_auto_20161230_1907.py
# Compiled at: 2016-12-30 13:07:28
# Size of source mod 2**32: 1139 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('shop', '0005_auto_20161230_1833')]
    operations = [
     migrations.RemoveField(model_name='cart', name='_products'),
     migrations.AddField(model_name='orderproduct', name='quantity', field=models.PositiveSmallIntegerField(default=1, verbose_name='quantity'), preserve_default=False),
     migrations.AddField(model_name='orderproduct', name='subtotal', field=models.DecimalField(decimal_places=2, default=1, max_digits=18, verbose_name='subtotal'), preserve_default=False),
     migrations.AddField(model_name='orderproduct', name='unit_price', field=models.DecimalField(decimal_places=2, default=1, max_digits=18, verbose_name='unit price'), preserve_default=False)]