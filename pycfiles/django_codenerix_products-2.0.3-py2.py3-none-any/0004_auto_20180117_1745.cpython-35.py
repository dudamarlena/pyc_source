# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_products/migrations/0004_auto_20180117_1745.py
# Compiled at: 2018-01-17 11:45:18
# Size of source mod 2**32: 1936 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_products', '0003_auto_20180117_1655')]
    operations = [
     migrations.AlterField(model_name='attribute', name='price', field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Price')),
     migrations.AlterField(model_name='feature', name='price', field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Price')),
     migrations.AlterField(model_name='featurespecial', name='price', field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Price')),
     migrations.AlterField(model_name='product', name='price_base', field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Price base')),
     migrations.AlterField(model_name='productfinal', name='price', field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10, verbose_name='Price')),
     migrations.AlterField(model_name='productfinal', name='price_base', field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10, verbose_name='Price base')),
     migrations.AlterField(model_name='productfinal', name='price_base_local', field=models.DecimalField(blank=True, decimal_places=2, help_text='If it is empty, price base is equal to price base of product', max_digits=10, null=True, verbose_name='Price base'))]