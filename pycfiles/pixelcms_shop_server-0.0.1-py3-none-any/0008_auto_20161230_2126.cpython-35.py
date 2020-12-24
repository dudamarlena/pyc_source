# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/migrations/0008_auto_20161230_2126.py
# Compiled at: 2016-12-30 15:26:12
# Size of source mod 2**32: 573 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('shop', '0007_auto_20161230_2117')]
    operations = [
     migrations.AlterField(model_name='orderproduct', name='product', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Product', verbose_name='product'))]