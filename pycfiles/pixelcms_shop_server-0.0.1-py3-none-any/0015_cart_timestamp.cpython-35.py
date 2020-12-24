# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/migrations/0015_cart_timestamp.py
# Compiled at: 2017-01-02 10:16:22
# Size of source mod 2**32: 458 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('shop', '0014_orderproduct_product_name')]
    operations = [
     migrations.AddField(model_name='cart', name='timestamp', field=models.DateTimeField(auto_now=True))]