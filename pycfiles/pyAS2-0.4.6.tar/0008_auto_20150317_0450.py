# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pyas2/migrations/0008_auto_20150317_0450.py
# Compiled at: 2017-03-06 23:12:21
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('pyas2', '0007_auto_20150313_0707')]
    operations = [
     migrations.AlterField(model_name=b'partner', name=b'mdn_mode', field=models.CharField(blank=True, max_length=20, null=True, choices=[('SYNC', 'Synchronous'), ('ASYNC', 'Asynchronous')]), preserve_default=True),
     migrations.AlterField(model_name=b'partner', name=b'mdn_sign', field=models.CharField(blank=True, max_length=20, null=True, verbose_name=b'Request Signed MDN', choices=[('sha1', 'SHA-1')]), preserve_default=True)]