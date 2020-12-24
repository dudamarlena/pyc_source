# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_pos/migrations/0002_auto_20180227_0912.py
# Compiled at: 2018-02-27 03:12:45
# Size of source mod 2**32: 1095 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_pos', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='pos', name='hardware', field=models.ManyToManyField(blank=True, related_name='poss', to='codenerix_pos.POSHardware', verbose_name='Hardware it can use')),
     migrations.AlterField(model_name='pos', name='storage_query', field=models.ManyToManyField(blank=True, related_name='poss_storage_query', to='codenerix_storages.Storage', verbose_name='Storages where you can consult')),
     migrations.AlterField(model_name='pos', name='storage_stock', field=models.ManyToManyField(blank=True, related_name='poss_storage_stock', to='codenerix_storages.Storage', verbose_name='Storages where the stock is subtracted'))]