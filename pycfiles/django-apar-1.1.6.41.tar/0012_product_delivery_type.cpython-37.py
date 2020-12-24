# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0012_product_delivery_type.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 516 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0011_auto_20181202_1543')]
    operations = [
     migrations.AddField(model_name='product',
       name='delivery_type',
       field=models.CharField(blank=True, choices=[('sh', 'Shippable'), ('dw', 'Downloadable')], max_length=10, verbose_name='Delivery type'))]