# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/importer/osgeo_importer/migrations/0006_auto_20161007_1723.py
# Compiled at: 2016-11-01 16:45:08
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('osgeo_importer', '0005_uploadlayer_layer_name')]
    operations = [
     migrations.AlterField(model_name=b'uploadeddata', name=b'upload_dir', field=models.CharField(max_length=1000, null=True))]