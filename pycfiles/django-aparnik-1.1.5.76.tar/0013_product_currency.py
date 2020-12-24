# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0013_product_currency.py
# Compiled at: 2019-01-31 06:07:32
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0012_product_delivery_type')]
    operations = [
     migrations.AddField(model_name=b'product', name=b'currency', field=models.CharField(choices=[('IRR', 'IRR'), ('D', 'Dollar')], default=b'IRR', max_length=10, verbose_name=b'Currency'))]