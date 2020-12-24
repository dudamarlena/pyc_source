# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0042_auto_20200205_1455.py
# Compiled at: 2020-02-05 19:43:26
# Size of source mod 2**32: 1304 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0041_merge_20200204_1546')]
    operations = [
     migrations.CreateModel(name='Role',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=200)),
      (
       'active', models.BooleanField(default=True)),
      (
       'description', models.CharField(blank=True, max_length=200, null=True)),
      (
       'hourly_factor', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
      (
       'hourly_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
      (
       'role_type', models.PositiveIntegerField(blank=True, null=True)),
      (
       'system_role', models.BooleanField(default=False))]),
     migrations.AddField(model_name='timeentry',
       name='role',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.Role'))]