# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0098_auto_20190718_1406.py
# Compiled at: 2019-08-14 13:00:26
# Size of source mod 2**32: 653 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0097_merge_20190718_1325')]
    operations = [
     migrations.RemoveField(model_name='ticket',
       name='agreement_id'),
     migrations.AddField(model_name='ticket',
       name='agreement',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), related_name='agreement_tickets', to='djconnectwise.Agreement'))]