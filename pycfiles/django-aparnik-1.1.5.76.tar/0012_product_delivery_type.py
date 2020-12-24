# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0012_product_delivery_type.py
# Compiled at: 2019-01-31 06:07:32
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0011_auto_20181202_1543')]
    operations = [
     migrations.AddField(model_name=b'product', name=b'delivery_type', field=models.CharField(blank=True, choices=[('sh', 'Shippable'), ('dw', 'Downloadable')], max_length=10, verbose_name=b'Delivery type'))]