# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0109_ticket_phase.py
# Compiled at: 2019-08-21 18:56:27
# Size of source mod 2**32: 535 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0108_projectphase')]
    operations = [
     migrations.AddField(model_name='ticket',
       name='phase',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), related_name='phase_tickets', to='djconnectwise.ProjectPhase'))]