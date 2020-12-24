# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/importer/osgeo_importer/migrations/0008_uploadlayer_import_status.py
# Compiled at: 2016-11-01 16:45:08
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('osgeo_importer', '0007_auto_20161025_2130')]
    operations = [
     migrations.AddField(model_name=b'uploadlayer', name=b'import_status', field=models.CharField(max_length=15, null=True, blank=True))]