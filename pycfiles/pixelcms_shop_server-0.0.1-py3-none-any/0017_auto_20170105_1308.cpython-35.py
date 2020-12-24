# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/migrations/0017_auto_20170105_1308.py
# Compiled at: 2017-01-05 07:08:57
# Size of source mod 2**32: 567 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('shop', '0016_category_thumbnail')]
    operations = [
     migrations.AlterField(model_name='cartproduct', name='product', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_products', to='shop.Product'))]