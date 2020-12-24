# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0009_auto_20181130_2025.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1156 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0008_product_further_details')]
    operations = [
     migrations.AddField(model_name='product',
       name='aparnik_bon_return_expire_value',
       field=models.PositiveIntegerField(default=0, help_text='If the number is set to 0, then the value in the settings will apply', verbose_name='Bon Return Expire ( Hours )')),
     migrations.AddField(model_name='product',
       name='aparnik_bon_return_value',
       field=models.PositiveIntegerField(default=0, help_text='If the number is set to 0, then the value in the settings will apply', verbose_name='Bon Return')),
     migrations.AddField(model_name='product',
       name='has_permit_use_aparnik_bon_value',
       field=models.NullBooleanField(help_text='If the number is set to 0, then the value in the settings will apply', verbose_name='Has permit use aparnik bon'))]