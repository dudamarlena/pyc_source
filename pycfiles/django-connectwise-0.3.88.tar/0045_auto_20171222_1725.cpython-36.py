# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0045_auto_20171222_1725.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 861 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0044_auto_20171222_1700')]
    operations = [
     migrations.AddField(model_name='project',
       name='actual_hours',
       field=models.DecimalField(max_digits=6, blank=True, null=True, decimal_places=2)),
     migrations.AddField(model_name='project',
       name='budget_hours',
       field=models.DecimalField(max_digits=6, blank=True, null=True, decimal_places=2)),
     migrations.AddField(model_name='project',
       name='scheduled_hours',
       field=models.DecimalField(max_digits=6, blank=True, null=True, decimal_places=2))]