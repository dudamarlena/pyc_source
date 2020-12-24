# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/file/migrations/0003_file_original_name.py
# Compiled at: 2015-01-20 14:25:09
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('file', '0002_file_mimetype')]
    operations = [
     migrations.AddField(model_name=b'file', name=b'original_name', field=models.CharField(default=b'', max_length=255), preserve_default=False)]