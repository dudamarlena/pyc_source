# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0008_product_further_details.py
# Compiled at: 2018-11-16 05:29:39
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0007_auto_20181114_1230')]
    operations = [
     migrations.AddField(model_name=b'product', name=b'further_details', field=models.TextField(blank=True, null=True, verbose_name=b'Extra Description'))]