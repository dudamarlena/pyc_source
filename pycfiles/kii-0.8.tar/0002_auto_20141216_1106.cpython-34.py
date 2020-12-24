# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/migrations/0002_auto_20141216_1106.py
# Compiled at: 2015-01-17 16:40:50
# Size of source mod 2**32: 1509 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('stream', '0001_initial')]
    operations = [
     migrations.AddField(model_name='stream', name='_content_rendered', field=models.TextField(default=''), preserve_default=True),
     migrations.AddField(model_name='stream', name='content_markup_type', field=models.CharField(default='markdown', max_length=255), preserve_default=True),
     migrations.AddField(model_name='streamitem', name='_content_rendered', field=models.TextField(default=''), preserve_default=True),
     migrations.AddField(model_name='streamitem', name='content_markup_type', field=models.CharField(default='markdown', max_length=255), preserve_default=True),
     migrations.AddField(model_name='streamitemcomment', name='_content_rendered', field=models.TextField(default=''), preserve_default=True),
     migrations.AddField(model_name='streamitemcomment', name='content_markup_type', field=models.CharField(default='markdown', max_length=255), preserve_default=True)]