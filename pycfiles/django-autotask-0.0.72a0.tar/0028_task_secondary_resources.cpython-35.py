# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0028_task_secondary_resources.py
# Compiled at: 2019-12-04 18:09:39
# Size of source mod 2**32: 501 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0027_auto_20191125_1103')]
    operations = [
     migrations.AddField(model_name='task', name='secondary_resources', field=models.ManyToManyField(related_name='secondary_resource_tasks', through='djautotask.TaskSecondaryResource', to='djautotask.Resource'))]