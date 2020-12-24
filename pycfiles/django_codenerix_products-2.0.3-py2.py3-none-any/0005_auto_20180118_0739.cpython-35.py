# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_products/migrations/0005_auto_20180118_0739.py
# Compiled at: 2018-01-18 01:39:33
# Size of source mod 2**32: 834 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_products', '0004_auto_20180117_1745')]
    operations = [
     migrations.AlterField(model_name='attribute', name='price', field=models.FloatField(default=0, verbose_name='Price')),
     migrations.AlterField(model_name='feature', name='price', field=models.FloatField(default=0, verbose_name='Price')),
     migrations.AlterField(model_name='featurespecial', name='price', field=models.FloatField(default=0, verbose_name='Price'))]