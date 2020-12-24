# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0030_task_phase.py
# Compiled at: 2019-11-28 12:57:57
# Size of source mod 2**32: 490 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0029_phase_last_activity_date')]
    operations = [
     migrations.AddField(model_name='task', name='phase', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.Phase'))]