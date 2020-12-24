# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/umeboshi/migrations/0001_initial.py
# Compiled at: 2015-12-31 08:38:34
from __future__ import unicode_literals
from django.db import migrations, models
import django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Event', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'uuid', django_extensions.db.fields.ShortUUIDField(unique=True, editable=False, blank=True)),
      (
       b'trigger_name', models.CharField(max_length=50, db_index=True)),
      (
       b'task_group', models.CharField(max_length=256, null=True, db_index=True)),
      (
       b'data_pickled', models.TextField(editable=False, blank=True)),
      (
       b'data_hash', models.CharField(max_length=32, db_index=True)),
      (
       b'datetime_created', models.DateTimeField(auto_now_add=True, null=True)),
      (
       b'datetime_scheduled', models.DateTimeField(db_index=True)),
      (
       b'datetime_processed', models.DateTimeField(null=True, db_index=True)),
      (
       b'status', models.IntegerField(default=0, db_index=True))]),
     migrations.AlterIndexTogether(name=b'event', index_together=set([('datetime_processed', 'datetime_scheduled'), ('data_hash', 'datetime_processed', 'trigger_name')]))]