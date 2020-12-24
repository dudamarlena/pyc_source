# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/forman/migrations/0002_auto_20170502_1406.py
# Compiled at: 2017-05-08 12:16:33
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('forman', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'survey', name=b'footer_image', field=models.FileField(blank=True, null=True, upload_to=b'')),
     migrations.AddField(model_name=b'survey', name=b'footer_message', field=models.CharField(blank=True, max_length=200)),
     migrations.AlterField(model_name=b'survey', name=b'header_image', field=models.FileField(blank=True, null=True, upload_to=b''))]