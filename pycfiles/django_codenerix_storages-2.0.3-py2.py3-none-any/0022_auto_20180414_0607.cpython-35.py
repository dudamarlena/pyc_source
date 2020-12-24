# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0022_auto_20180414_0607.py
# Compiled at: 2018-04-14 00:07:57
# Size of source mod 2**32: 920 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0021_auto_20180413_1825')]
    operations = [
     migrations.AddField(model_name='inventory', name='processed', field=models.BooleanField(default=False, editable=False, verbose_name='Processed')),
     migrations.AddField(model_name='inventoryin', name='processed', field=models.BooleanField(default=False, editable=False, verbose_name='Processed')),
     migrations.AddField(model_name='inventoryout', name='processed', field=models.BooleanField(default=False, editable=False, verbose_name='Processed'))]