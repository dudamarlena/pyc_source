# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/importer/osgeo_importer/migrations/0002_auto_20160713_1429.py
# Compiled at: 2016-07-18 17:07:14
from __future__ import unicode_literals
from django.db import migrations, models
import jsonfield.fields

class Migration(migrations.Migration):
    dependencies = [
     ('osgeo_importer', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'uploadlayer', name=b'fields', field=jsonfield.fields.JSONField(default={}, null=True))]