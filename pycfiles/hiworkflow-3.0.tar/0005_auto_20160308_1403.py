# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hasher/apps/workflow/workflowapp/migrations/0005_auto_20160308_1403.py
# Compiled at: 2016-03-08 09:03:57
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('workflowapp', '0004_auto_20160308_0952')]
    operations = [
     migrations.AlterField(model_name=b'task', name=b'current_state', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=b'workflowapp.State'))]