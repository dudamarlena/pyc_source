# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/migrations/0014_orderproduct_product_name.py
# Compiled at: 2016-12-30 16:22:15
# Size of source mod 2**32: 529 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('shop', '0013_auto_20161230_2219')]
    operations = [
     migrations.AddField(model_name='orderproduct', name='product_name', field=models.CharField(default=' ', max_length=255, verbose_name='name'), preserve_default=False)]