# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0024_auto_20180426_1034.py
# Compiled at: 2018-04-26 04:34:46
# Size of source mod 2**32: 926 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0023_auto_20180414_1252')]
    operations = [
     migrations.AddField(model_name='inventory', name='storage', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventorys', to='codenerix_storages.Storage', verbose_name='Storage')),
     migrations.AddField(model_name='inventory', name='zone', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventorys', to='codenerix_storages.StorageZone', verbose_name='Zone'))]