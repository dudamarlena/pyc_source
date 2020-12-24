# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0037_subissuetype_parent_value.py
# Compiled at: 2020-01-29 13:32:26
# Size of source mod 2**32: 514 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0036_auto_20200127_1157')]
    operations = [
     migrations.AddField(model_name='subissuetype',
       name='parent_value',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='djautotask.IssueType'))]