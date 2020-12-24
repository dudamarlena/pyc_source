# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/migrations/0002_auto_20161230_1608.py
# Compiled at: 2016-12-30 10:08:45
# Size of source mod 2**32: 1094 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('shop', '0001_initial')]
    operations = [
     migrations.CreateModel(name='OrderProduct', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.Order')),
      (
       'product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product', verbose_name='product'))], options={'verbose_name': 'product', 
      'ordering': ('pk', ), 
      'verbose_name_plural': 'products'}),
     migrations.RemoveField(model_name='cart', name='converted_to_order')]