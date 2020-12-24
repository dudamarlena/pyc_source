# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/migrations/0020_auto_20170110_1739.py
# Compiled at: 2017-01-10 11:39:12
# Size of source mod 2**32: 1482 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('shop', '0019_auto_20170110_1729')]
    operations = [
     migrations.RemoveField(model_name='customer', name='address'),
     migrations.RemoveField(model_name='customer', name='phone'),
     migrations.RemoveField(model_name='customer', name='place'),
     migrations.RemoveField(model_name='customer', name='postal_code'),
     migrations.AlterField(model_name='cart', name='customer', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='shop.Customer', verbose_name='customer')),
     migrations.AlterField(model_name='order', name='customer', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='shop.Customer', verbose_name='customer')),
     migrations.AlterField(model_name='order', name='order_id', field=models.CharField(blank=True, max_length=255, null=True, verbose_name='order ID'))]