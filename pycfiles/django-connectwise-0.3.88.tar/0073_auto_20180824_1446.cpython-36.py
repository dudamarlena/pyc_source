# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0073_auto_20180824_1446.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1730 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0072_remove_callbackentry_member')]
    operations = [
     migrations.AddField(model_name='boardstatus',
       name='escalation_status',
       field=models.CharField(blank=True, choices=[('NotResponded', 'Not Responded'), ('Responded', 'Responded'), ('ResolutionPlan', 'Resolution Plan'), ('Resolved', 'Resolved'), ('NoEscalation', 'No Escalation')], db_index=True, max_length=20, null=True)),
     migrations.AddField(model_name='company',
       name='calendar',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djconnectwise.Calendar')),
     migrations.AddField(model_name='ticket',
       name='do_not_escalate_date',
       field=models.DateTimeField(blank=True, null=True)),
     migrations.AddField(model_name='ticket',
       name='minutes_waiting',
       field=models.PositiveIntegerField(default=0)),
     migrations.AddField(model_name='ticket',
       name='sla_expire_date',
       field=models.DateTimeField(blank=True, null=True)),
     migrations.AddField(model_name='ticket',
       name='sla_stage',
       field=models.CharField(blank=True, choices=[('respond', 'Respond'), ('plan', 'Plan'), ('resolve', 'Resolve'), ('resolved', 'Resolved'), ('waiting', 'Waiting')], db_index=True, max_length=250, null=True))]