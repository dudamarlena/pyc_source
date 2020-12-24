# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0017_auto_20190319_1744.py
# Compiled at: 2019-03-19 10:14:13
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0016_product_is_draft')]
    operations = [
     migrations.AlterField(model_name=b'product', name=b'is_draft', field=models.BooleanField(default=False, verbose_name=b'Is draft'))]