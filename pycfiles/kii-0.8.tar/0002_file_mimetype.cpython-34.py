# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/file/migrations/0002_file_mimetype.py
# Compiled at: 2015-01-18 14:53:14
# Size of source mod 2**32: 445 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('file', '0001_initial')]
    operations = [
     migrations.AddField(model_name='file', name='mimetype', field=models.CharField(default='text/plain', max_length=255), preserve_default=False)]