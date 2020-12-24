# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/migrations/0005_auto_20141217_1455.py
# Compiled at: 2014-12-31 04:01:41
# Size of source mod 2**32: 1683 bytes
from __future__ import unicode_literals
from django.db import models, migrations
import datetime

class Migration(migrations.Migration):
    dependencies = [
     ('stream', '0004_auto_20141217_1222')]
    operations = [
     migrations.AlterModelOptions(name='itemcomment', options={'ordering': ['created']}),
     migrations.RemoveField(model_name='itemcomment', name='junk'),
     migrations.RemoveField(model_name='itemcomment', name='published'),
     migrations.AddField(model_name='itemcomment', name='created', field=models.DateTimeField(default=datetime.datetime(2014, 12, 17, 14, 55, 24, 847315), auto_now_add=True), preserve_default=False),
     migrations.AddField(model_name='itemcomment', name='last_modified', field=models.DateTimeField(default=datetime.datetime(2014, 12, 17, 14, 55, 34, 791525), auto_now=True), preserve_default=False),
     migrations.AddField(model_name='itemcomment', name='publication_date', field=models.DateTimeField(default=None, null=True, editable=False, blank=True), preserve_default=True),
     migrations.AddField(model_name='itemcomment', name='status', field=models.CharField(default='dra', max_length=5, choices=[('dra', 'base_models.status_mixin.draft'), ('pub', 'base_models.status_mixin.published')]), preserve_default=True)]