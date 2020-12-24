# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/importer/osgeo_importer/migrations/0005_uploadlayer_layer_name.py
# Compiled at: 2016-09-29 16:34:19
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('osgeo_importer', '0004_uploadfile_file_type')]
    operations = [
     migrations.AddField(model_name=b'uploadlayer', name=b'layer_name', field=models.CharField(max_length=64, null=True))]