# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0018_auto_20190423_1058.py
# Compiled at: 2019-04-23 02:28:02
from __future__ import unicode_literals
import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0017_auto_20190319_1744')]
    operations = [
     migrations.AlterField(model_name=b'product', name=b'aparnik_bon_return_value', field=models.IntegerField(default=-1, help_text=b'If the number is set to -1, then the value in the settings will apply', validators=[django.core.validators.MinValueValidator(-1), django.core.validators.MaxValueValidator(100)], verbose_name=b'Bon Return')),
     migrations.AlterField(model_name=b'product', name=b'maximum_use_aparnik_bon_value', field=models.IntegerField(default=-1, help_text=b'If the number is set to -1, then the value in the settings will apply, If the number is set to -2, then no limitation execution.', validators=[django.core.validators.MinValueValidator(-2), django.core.validators.MaxValueValidator(100)], verbose_name=b'Maximum use aparnik bon'))]