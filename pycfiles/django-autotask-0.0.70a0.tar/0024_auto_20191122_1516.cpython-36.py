# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0024_auto_20191122_1516.py
# Compiled at: 2019-11-28 19:04:27
# Size of source mod 2**32: 3582 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    atomic = False
    dependencies = [
     ('djautotask', '0023_auto_20191119_0923')]
    operations = [
     migrations.RenameModel(old_name='TicketStatus',
       new_name='Status'),
     migrations.AlterModelOptions(name='status',
       options={'verbose_name_plural': 'Statuses'}),
     migrations.CreateModel(name='Task',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'title', models.CharField(blank=True, max_length=255, null=True)),
      (
       'number', models.CharField(blank=True, max_length=50, null=True)),
      (
       'description', models.CharField(blank=True, max_length=8000, null=True)),
      (
       'completed_date', models.DateTimeField(blank=True, null=True)),
      (
       'create_date', models.DateTimeField(blank=True, null=True)),
      (
       'start_date', models.DateTimeField(blank=True, null=True)),
      (
       'end_date', models.DateTimeField(blank=True, null=True)),
      (
       'estimated_hours', models.PositiveIntegerField(default=0)),
      (
       'remaining_hours', models.PositiveIntegerField(default=0)),
      (
       'last_activity_date', models.DateTimeField(blank=True, null=True)),
      (
       'assigned_resource', models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.Resource')),
      (
       'priority_label', models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.TicketPriority')),
      (
       'project', models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.Project'))],
       options={'ordering':('-modified', '-created'), 
      'get_latest_by':'modified', 
      'abstract':False}),
     migrations.CreateModel(name='TaskSecondaryResource',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'resource', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.Resource')),
      (
       'task', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.Task'))],
       options={'ordering':('-modified', '-created'), 
      'get_latest_by':'modified', 
      'abstract':False}),
     migrations.AddField(model_name='task',
       name='status',
       field=models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.Status'))]