# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0051_auto_20200315_1819.py
# Compiled at: 2020-03-24 16:47:33
# Size of source mod 2**32: 754 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0050_remove_ticket_role')]
    operations = [
     migrations.AddField(model_name='tasksecondaryresource',
       name='role',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.Role')),
     migrations.AddField(model_name='ticketsecondaryresource',
       name='role',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.Role'))]