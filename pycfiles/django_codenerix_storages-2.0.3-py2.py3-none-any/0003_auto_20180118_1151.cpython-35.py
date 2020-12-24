# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0003_auto_20180118_1151.py
# Compiled at: 2018-01-18 06:07:56
# Size of source mod 2**32: 1030 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0002_auto_20180118_1040')]
    operations = [
     migrations.RemoveField(model_name='storage', name='alias'),
     migrations.AlterField(model_name='storagebox', name='box_kind', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storage_boxes', to='codenerix_storages.StorageBoxKind', verbose_name='Box Kind')),
     migrations.AlterField(model_name='storagebox', name='box_structure', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storage_boxes', to='codenerix_storages.StorageBoxStructure', verbose_name='Box Structure'))]