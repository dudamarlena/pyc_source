# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hasher/apps/workflow/workflowapp/migrations/0002_trigger.py
# Compiled at: 2016-03-04 08:11:07
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('workflowapp', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'Trigger', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'trigger_function', models.CharField(max_length=100, null=True)),
      (
       b'state_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'workflowapp.State'))])]