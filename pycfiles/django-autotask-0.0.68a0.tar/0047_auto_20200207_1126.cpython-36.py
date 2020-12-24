# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0047_auto_20200207_1126.py
# Compiled at: 2020-02-28 16:41:52
# Size of source mod 2**32: 762 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0046_auto_20200207_1002')]
    operations = [
     migrations.AddField(model_name='task',
       name='allocation_code',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.AllocationCode')),
     migrations.AddField(model_name='ticket',
       name='allocation_code',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.AllocationCode'))]