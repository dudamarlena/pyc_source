# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0051_auto_20200315_1819.py
# Compiled at: 2020-05-08 13:23:41
# Size of source mod 2**32: 754 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0050_remove_ticket_role')]
    operations = [
     migrations.AddField(model_name='tasksecondaryresource', name='role', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.Role')),
     migrations.AddField(model_name='ticketsecondaryresource', name='role', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.Role'))]