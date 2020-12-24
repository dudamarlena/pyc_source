# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0029_phase_last_activity_date.py
# Compiled at: 2019-12-02 13:16:21
# Size of source mod 2**32: 398 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0028_phase')]
    operations = [
     migrations.AddField(model_name='phase',
       name='last_activity_date',
       field=models.DateTimeField(blank=True, null=True))]