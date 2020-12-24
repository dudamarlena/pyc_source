# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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