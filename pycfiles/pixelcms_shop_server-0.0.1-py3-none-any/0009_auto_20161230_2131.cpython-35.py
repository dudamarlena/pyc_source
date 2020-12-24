# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/migrations/0009_auto_20161230_2131.py
# Compiled at: 2016-12-30 15:31:00
# Size of source mod 2**32: 969 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('shop', '0008_auto_20161230_2126')]
    operations = [
     migrations.AlterModelOptions(name='cartproduct', options={'ordering': ('pk', ), 'verbose_name': 'cart product', 'verbose_name_plural': 'cart products'}),
     migrations.AlterModelOptions(name='orderproduct', options={'ordering': ('pk', ), 'verbose_name': 'order product', 'verbose_name_plural': 'order products'}),
     migrations.AlterField(model_name='orderproduct', name='product', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Product', verbose_name='product'))]