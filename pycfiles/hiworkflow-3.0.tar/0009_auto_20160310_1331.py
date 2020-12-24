# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hasher/apps/workflow/workflowapp/migrations/0009_auto_20160310_1331.py
# Compiled at: 2016-03-10 08:36:20
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('workflowapp', '0008_auto_20160309_1228')]
    operations = [
     migrations.RenameModel(old_name=b'Precondition', new_name=b'Condition'),
     migrations.RemoveField(model_name=b'condition', name=b'state_id'),
     migrations.AddField(model_name=b'condition', name=b'transition_id', field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=b'workflowapp.Transition'), preserve_default=False)]