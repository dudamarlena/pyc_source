# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0113_auto_20200204_1054.py
# Compiled at: 2020-02-05 12:45:52
# Size of source mod 2**32: 530 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0112_syncjob_synchronizer_class')]
    operations = [
     migrations.AlterField(model_name='opportunity',
       name='stage',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djconnectwise.OpportunityStage'))]