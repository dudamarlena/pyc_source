# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/migrations/0005_auto_20161230_1833.py
# Compiled at: 2016-12-30 12:33:06
# Size of source mod 2**32: 601 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('shop', '0004_order_customer')]
    operations = [
     migrations.AlterField(model_name='order', name='customer', field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.Customer', verbose_name='customer'), preserve_default=False)]