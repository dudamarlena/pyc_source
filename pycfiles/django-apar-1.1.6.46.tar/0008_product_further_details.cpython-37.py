# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0008_product_further_details.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 463 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0007_auto_20181114_1230')]
    operations = [
     migrations.AddField(model_name='product',
       name='further_details',
       field=models.TextField(blank=True, null=True, verbose_name='Extra Description'))]