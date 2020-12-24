# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_products/migrations/0009_auto_20180201_1137.py
# Compiled at: 2018-02-02 06:33:32
# Size of source mod 2**32: 814 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_products', '0008_auto_20180126_1711')]
    operations = [
     migrations.AlterField(model_name='productunique', name='box', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_unique', to='codenerix_storages.StorageBox', verbose_name='Box')),
     migrations.AlterField(model_name='productunique', name='stock_original', field=models.FloatField(default=0, verbose_name='Stock original'))]