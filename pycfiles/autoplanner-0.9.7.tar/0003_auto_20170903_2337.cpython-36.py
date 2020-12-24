# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/AutoPlanner/autoplanner/migrations/0003_auto_20170903_2337.py
# Compiled at: 2017-09-03 17:37:42
# Size of source mod 2**32: 551 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('autoplanner', '0002_auto_20170903_2258')]
    operations = [
     migrations.AlterField(model_name='schedulerun',
       name='celery_task_id',
       field=models.CharField(blank=True, db_index=True, default=None, max_length=60, null=True, verbose_name='Celery task id'))]