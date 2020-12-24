# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./pyas2/migrations/0004_auto_20150311_1258.py
# Compiled at: 2017-03-06 23:12:21
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('pyas2', '0003_auto_20150311_1141')]
    operations = [
     migrations.RemoveField(model_name=b'message', name=b'encryption'),
     migrations.RemoveField(model_name=b'message', name=b'signature'),
     migrations.AddField(model_name=b'mdn', name=b'signed', field=models.BooleanField(default=False), preserve_default=True),
     migrations.AddField(model_name=b'message', name=b'encrypted', field=models.BooleanField(default=False), preserve_default=True),
     migrations.AddField(model_name=b'message', name=b'signed', field=models.BooleanField(default=False), preserve_default=True)]