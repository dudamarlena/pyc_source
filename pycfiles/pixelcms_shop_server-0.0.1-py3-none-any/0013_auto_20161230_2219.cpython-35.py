# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/migrations/0013_auto_20161230_2219.py
# Compiled at: 2016-12-30 16:19:04
# Size of source mod 2**32: 1667 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('shop', '0012_auto_20161230_2136')]
    operations = [
     migrations.CreateModel(name='OrderProductOption', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'options_group', models.CharField(max_length=255, verbose_name='options group')),
      (
       'option', models.CharField(max_length=255, verbose_name='option')),
      (
       'price_mod', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True, verbose_name='price modification')),
      (
       'price_mod_percentage', models.BooleanField(default=False, verbose_name='percentage')),
      (
       'order_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='shop.OrderProduct'))], options={'verbose_name_plural': 'options', 
      'ordering': ('pk', ), 
      'verbose_name': 'option'}),
     migrations.AlterModelOptions(name='orderbillingdata', options={'verbose_name': 'billing data', 'verbose_name_plural': 'billing data'}),
     migrations.AlterModelOptions(name='ordershippingdata', options={'verbose_name': 'shipping data', 'verbose_name_plural': 'shipping data'})]