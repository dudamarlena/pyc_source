# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0015_auto_20190129_1728.py
# Compiled at: 2019-01-31 06:07:32
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0014_product_is_tax')]
    operations = [
     migrations.AlterField(model_name=b'product', name=b'maximum_use_aparnik_bon_value', field=models.IntegerField(default=-1, help_text=b'If the number is set to -1, then the value in the settings will apply, If the number is set to -2, then no limitation execution.', verbose_name=b'Maximum use aparnik bon'))]