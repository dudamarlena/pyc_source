# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0008_project_status_name.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 436 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0007_auto_20170311_1415')]
    operations = [
     migrations.AddField(model_name='project',
       name='status_name',
       field=models.CharField(max_length=200, blank=True, null=True))]