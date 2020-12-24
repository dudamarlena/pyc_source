# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0021_auto_20180413_1825.py
# Compiled at: 2018-04-13 12:25:19
# Size of source mod 2**32: 863 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0020_auto_20180413_1642')]
    operations = [
     migrations.AddField(model_name='inventory', name='notes', field=models.TextField(blank=True, null=True, verbose_name='Notes')),
     migrations.AddField(model_name='inventoryin', name='notes', field=models.TextField(blank=True, null=True, verbose_name='Notes')),
     migrations.AddField(model_name='inventoryout', name='notes', field=models.TextField(blank=True, null=True, verbose_name='Notes'))]