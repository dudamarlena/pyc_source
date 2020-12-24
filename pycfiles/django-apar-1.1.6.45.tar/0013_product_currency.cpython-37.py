# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0013_product_currency.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 500 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0012_product_delivery_type')]
    operations = [
     migrations.AddField(model_name='product',
       name='currency',
       field=models.CharField(choices=[('IRR', 'IRR'), ('D', 'Dollar')], default='IRR', max_length=10, verbose_name='Currency'))]