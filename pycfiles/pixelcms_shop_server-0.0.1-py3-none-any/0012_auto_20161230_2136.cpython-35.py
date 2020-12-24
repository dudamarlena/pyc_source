# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/migrations/0012_auto_20161230_2136.py
# Compiled at: 2016-12-30 15:36:59
# Size of source mod 2**32: 1150 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('shop', '0011_auto_20161230_2135')]
    operations = [
     migrations.AlterModelOptions(name='orderbillingdata', options={'verbose_name': '', 'verbose_name_plural': 'billing data'}),
     migrations.AlterModelOptions(name='ordershippingdata', options={'verbose_name': '', 'verbose_name_plural': 'shipping data'}),
     migrations.AlterField(model_name='orderbillingdata', name='order', field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='billing_data', to='shop.Order')),
     migrations.AlterField(model_name='ordershippingdata', name='order', field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_data', to='shop.Order'))]