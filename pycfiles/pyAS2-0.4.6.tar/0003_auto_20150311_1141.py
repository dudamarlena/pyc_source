# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pyas2/migrations/0003_auto_20150311_1141.py
# Compiled at: 2017-03-06 23:12:21
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('pyas2', '0002_partner_compress')]
    operations = [
     migrations.AddField(model_name=b'message', name=b'encryption', field=models.CharField(max_length=20, null=True, blank=True), preserve_default=True),
     migrations.AddField(model_name=b'message', name=b'signature', field=models.CharField(max_length=20, null=True, blank=True), preserve_default=True)]