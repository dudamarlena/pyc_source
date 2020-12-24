# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/migrations/0005_auto_20141217_1455.py
# Compiled at: 2014-12-31 04:01:41
from __future__ import unicode_literals
from django.db import models, migrations
import datetime

class Migration(migrations.Migration):
    dependencies = [
     ('stream', '0004_auto_20141217_1222')]
    operations = [
     migrations.AlterModelOptions(name=b'itemcomment', options={b'ordering': [b'created']}),
     migrations.RemoveField(model_name=b'itemcomment', name=b'junk'),
     migrations.RemoveField(model_name=b'itemcomment', name=b'published'),
     migrations.AddField(model_name=b'itemcomment', name=b'created', field=models.DateTimeField(default=datetime.datetime(2014, 12, 17, 14, 55, 24, 847315), auto_now_add=True), preserve_default=False),
     migrations.AddField(model_name=b'itemcomment', name=b'last_modified', field=models.DateTimeField(default=datetime.datetime(2014, 12, 17, 14, 55, 34, 791525), auto_now=True), preserve_default=False),
     migrations.AddField(model_name=b'itemcomment', name=b'publication_date', field=models.DateTimeField(default=None, null=True, editable=False, blank=True), preserve_default=True),
     migrations.AddField(model_name=b'itemcomment', name=b'status', field=models.CharField(default=b'dra', max_length=5, choices=[('dra', 'base_models.status_mixin.draft'), ('pub', 'base_models.status_mixin.published')]), preserve_default=True)]