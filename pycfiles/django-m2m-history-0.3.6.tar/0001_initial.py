# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-m2m-history/m2m_history/migrations/0001_initial.py
# Compiled at: 2016-02-26 14:17:16
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'ManyToManyHistoryVersion', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'object_id', models.BigIntegerField(db_index=True)),
      (
       b'field_name', models.CharField(max_length=50, db_index=True)),
      (
       b'time', models.DateTimeField(db_index=True)),
      (
       b'count', models.PositiveIntegerField(default=0)),
      (
       b'added_count', models.PositiveIntegerField(default=0)),
      (
       b'removed_count', models.PositiveIntegerField(default=0)),
      (
       b'content_type', models.ForeignKey(related_name=b'm2m_history_versions', to=b'contenttypes.ContentType'))], options={}, bases=(
      models.Model,)),
     migrations.AlterUniqueTogether(name=b'manytomanyhistoryversion', unique_together=set([('content_type', 'object_id', 'field_name', 'time')]))]