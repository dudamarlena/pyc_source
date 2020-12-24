# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/workers/migrations/0001_initial.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 1310 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Worker',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=30)),
      (
       'provider', models.CharField(max_length=30)),
      (
       'type', models.CharField(max_length=30)),
      (
       'n_tasks', models.IntegerField(blank=True, default=0, null=True)),
      (
       'status', models.CharField(max_length=30)),
      (
       'current_status', models.TextField(blank=True, null=True)),
      (
       'worker_id', models.CharField(max_length=30)),
      (
       'ip', models.CharField(max_length=30)),
      (
       'creation_date', models.DateTimeField(auto_now_add=True, null=True)),
      (
       'modified_date', models.DateTimeField(auto_now=True, null=True)),
      (
       'started', models.DateTimeField(null=True)),
      (
       'finished', models.DateTimeField(null=True)),
      (
       'execution_time', models.TimeField(null=True))])]