# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0029_auto_20170607_1147.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1217 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0028_merge')]
    operations = [
     migrations.AddField(model_name='syncjob',
       name='added',
       field=models.PositiveSmallIntegerField(null=True),
       preserve_default=False),
     migrations.AddField(model_name='syncjob',
       name='deleted',
       field=models.PositiveSmallIntegerField(null=True),
       preserve_default=False),
     migrations.AddField(model_name='syncjob',
       name='message',
       field=models.CharField(max_length=100, default=None, blank=True, null=True),
       preserve_default=False),
     migrations.AddField(model_name='syncjob',
       name='success',
       field=(models.NullBooleanField())),
     migrations.AddField(model_name='syncjob',
       name='updated',
       field=models.PositiveSmallIntegerField(null=True),
       preserve_default=False)]