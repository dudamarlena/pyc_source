# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hasher/apps/workflow/workflowapp/migrations/0001_initial.py
# Compiled at: 2016-03-04 08:11:07
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'Assignee', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'assignee_id', to=settings.AUTH_USER_MODEL))]),
     migrations.CreateModel(name=b'Permission', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'allow_access', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
      (
       b'deny_access', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'deny_access_user', to=settings.AUTH_USER_MODEL))]),
     migrations.CreateModel(name=b'Precondition', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'condition', models.CharField(max_length=100, null=True))]),
     migrations.CreateModel(name=b'State', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=100)),
      (
       b'is_start', models.BooleanField(default=False)),
      (
       b'is_end', models.BooleanField(default=False))]),
     migrations.CreateModel(name=b'Stateconnect', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'action', models.CharField(max_length=100)),
      (
       b'next_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'next_state_id', to=b'workflowapp.State')),
      (
       b'state_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'workflowapp.State'))]),
     migrations.CreateModel(name=b'Task', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=50, null=True)),
      (
       b'description', models.TextField(max_length=300)),
      (
       b'is_active', models.BooleanField(default=True)),
      (
       b'created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
      (
       b'current_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'workflowapp.State'))]),
     migrations.CreateModel(name=b'Workflow', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=100)),
      (
       b'description', models.TextField(max_length=300)),
      (
       b'tasktitle', models.CharField(max_length=100, null=True))]),
     migrations.AddField(model_name=b'task', name=b'workflow_id', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'workflowapp.Workflow')),
     migrations.AddField(model_name=b'stateconnect', name=b'workflow_id', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'workflowapp.Workflow')),
     migrations.AddField(model_name=b'state', name=b'workflow_id', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'workflowapp.Workflow')),
     migrations.AddField(model_name=b'precondition', name=b'state_id', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'workflowapp.State')),
     migrations.AddField(model_name=b'permission', name=b'task_id', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'workflowapp.Task')),
     migrations.AddField(model_name=b'assignee', name=b'task_id', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'workflowapp.Task'))]