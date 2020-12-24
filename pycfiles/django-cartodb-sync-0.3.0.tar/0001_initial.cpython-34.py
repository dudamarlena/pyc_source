# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eric/Documents/code/django-cartodb-sync/cartodbsync/migrations/0001_initial.py
# Compiled at: 2015-08-27 11:45:36
# Size of source mod 2**32: 1120 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name')]
    operations = [
     migrations.CreateModel(name='SyncEntry', fields=[
      (
       'id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
      (
       'object_id', models.PositiveIntegerField(blank=True, null=True)),
      (
       'status', models.CharField(max_length=20, blank=True, null=True, choices=[('pending delete', 'pending delete'), ('pending insert', 'pending insert'), ('pending update', 'pending update'), ('success', 'success'), ('fail', 'fail')])),
      (
       'added', models.DateTimeField(auto_now_add=True)),
      (
       'updated', models.DateTimeField(auto_now=True)),
      (
       'attempts', models.IntegerField(default=0)),
      (
       'content_type', models.ForeignKey(to='contenttypes.ContentType', blank=True, null=True))])]