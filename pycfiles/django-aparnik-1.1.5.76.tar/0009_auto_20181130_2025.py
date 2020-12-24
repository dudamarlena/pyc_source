# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0009_auto_20181130_2025.py
# Compiled at: 2018-12-03 11:15:34
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0008_product_further_details')]
    operations = [
     migrations.AddField(model_name=b'product', name=b'aparnik_bon_return_expire_value', field=models.PositiveIntegerField(default=0, help_text=b'If the number is set to 0, then the value in the settings will apply', verbose_name=b'Bon Return Expire ( Hours )')),
     migrations.AddField(model_name=b'product', name=b'aparnik_bon_return_value', field=models.PositiveIntegerField(default=0, help_text=b'If the number is set to 0, then the value in the settings will apply', verbose_name=b'Bon Return')),
     migrations.AddField(model_name=b'product', name=b'has_permit_use_aparnik_bon_value', field=models.NullBooleanField(help_text=b'If the number is set to 0, then the value in the settings will apply', verbose_name=b'Has permit use aparnik bon'))]