# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0032_auto_20170616_1144.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 571 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0031_auto_20170607_2234')]
    operations = [
     migrations.AlterField(model_name='ticket',
       name='record_type',
       field=models.CharField(null=True, blank=True, db_index=True, max_length=250, choices=[('ServiceTicket', 'Service Ticket'), ('ProjectTicket', 'Project Ticket'), ('ProjectIssue', 'Project Issue')]))]