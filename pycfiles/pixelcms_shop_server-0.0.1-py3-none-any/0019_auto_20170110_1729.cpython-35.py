# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/migrations/0019_auto_20170110_1729.py
# Compiled at: 2017-01-10 11:29:07
# Size of source mod 2**32: 827 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('shop', '0018_auto_20170110_1558')]
    operations = [
     migrations.AlterField(model_name='productattributevalue', name='attribute', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ProductAttribute', verbose_name='attribute')),
     migrations.AlterField(model_name='productsmoduleproduct', name='product', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product', verbose_name='product'))]