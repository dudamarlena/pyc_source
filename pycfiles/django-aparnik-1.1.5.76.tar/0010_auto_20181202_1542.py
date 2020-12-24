# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0010_auto_20181202_1542.py
# Compiled at: 2019-01-29 08:56:59
from __future__ import unicode_literals
import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0009_auto_20181130_2025')]
    operations = [
     migrations.RemoveField(model_name=b'product', name=b'has_permit_use_aparnik_bon_value'),
     migrations.AddField(model_name=b'product', name=b'has_permit_use_wallet_value', field=models.IntegerField(default=-1, help_text=b'If the number is set to -1, then the value in the settings will apply', validators=[django.core.validators.MaxValueValidator(1), django.core.validators.MinValueValidator(-1)], verbose_name=b'Has Permit use wallet')),
     migrations.AddField(model_name=b'product', name=b'maximum_use_aparnik_bon_value', field=models.IntegerField(default=-1, help_text=b'If the number is set to -1, then the value in the settings will apply', verbose_name=b'Maximum use aparnik bon')),
     migrations.AlterField(model_name=b'product', name=b'aparnik_bon_return_expire_value', field=models.IntegerField(default=-1, help_text=b'If the number is set to -1, then the value in the settings will apply', verbose_name=b'Bon Return Expire ( Hours )')),
     migrations.AlterField(model_name=b'product', name=b'aparnik_bon_return_value', field=models.IntegerField(default=-1, help_text=b'If the number is set to -1, then the value in the settings will apply', verbose_name=b'Bon Return'))]