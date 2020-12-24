# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0042_auto_20200205_1057.py
# Compiled at: 2020-02-06 12:37:08
# Size of source mod 2**32: 2395 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0041_merge_20200204_1546')]
    operations = [
     migrations.CreateModel(name='AllocationCode',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'name', models.CharField(blank=True, max_length=200, null=True)),
      (
       'description', models.CharField(blank=True, max_length=500, null=True)),
      (
       'active', models.BooleanField(default=False))],
       options={'ordering':('-modified', '-created'), 
      'get_latest_by':'modified', 
      'abstract':False}),
     migrations.CreateModel(name='UseType',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'label', models.CharField(blank=True, max_length=50, null=True)),
      (
       'is_default_value', models.BooleanField(default=False)),
      (
       'sort_order', models.PositiveSmallIntegerField(blank=True, null=True)),
      (
       'is_active', models.BooleanField(default=False)),
      (
       'is_system', models.BooleanField(default=False))],
       options={'ordering':('label', ), 
      'abstract':False}),
     migrations.AddField(model_name='allocationcode',
       name='use_type',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.UseType'))]