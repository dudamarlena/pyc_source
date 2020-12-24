# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0046_ticket_assigned_resource_role.py
# Compiled at: 2020-02-28 15:23:46
# Size of source mod 2**32: 542 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0045_resourceroledepartment_resourceservicedeskrole')]
    operations = [
     migrations.AddField(model_name='ticket', name='assigned_resource_role', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.Role'))]