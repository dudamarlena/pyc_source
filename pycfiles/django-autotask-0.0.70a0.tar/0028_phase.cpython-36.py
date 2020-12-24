# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0028_phase.py
# Compiled at: 2019-12-02 13:16:21
# Size of source mod 2**32: 1763 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0027_auto_20191125_1103')]
    operations = [
     migrations.CreateModel(name='Phase',
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
       'description', models.CharField(blank=True, max_length=8000, null=True)),
      (
       'start_date', models.DateTimeField(blank=True, null=True)),
      (
       'due_date', models.DateTimeField(blank=True, null=True)),
      (
       'estimated_hours', models.PositiveIntegerField(default=0)),
      (
       'number', models.CharField(blank=True, max_length=50, null=True)),
      (
       'scheduled', models.BooleanField(default=False)),
      (
       'parent_phase', models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.Phase')),
      (
       'project', models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.Project'))],
       options={'abstract':False, 
      'ordering':('-modified', '-created'), 
      'get_latest_by':'modified'})]