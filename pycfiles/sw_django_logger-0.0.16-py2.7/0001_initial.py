# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sw_logger/migrations/0001_initial.py
# Compiled at: 2018-02-07 05:07:39
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Log', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'action', models.CharField(choices=[('', ''), ('created', 'created'), ('updated', 'updated'), ('deleted', 'deleted')], default=b'', max_length=10)),
      (
       b'message', models.CharField(max_length=255)),
      (
       b'func_name', models.CharField(max_length=255)),
      (
       b'level', models.CharField(choices=[('', ''), ('CRITICAL', 'CRITICAL'), ('ERROR', 'ERROR'), ('WARNING', 'WARNING'), ('INFO', 'INFO'), ('DEBUG', 'DEBUG'), ('NOTSET', 'NOTSET')], default=b'NOTSET', max_length=10)),
      (
       b'http_general', models.TextField(blank=True)),
      (
       b'http_request_get', models.TextField(blank=True)),
      (
       b'http_request_post', models.TextField(blank=True)),
      (
       b'http_referrer', models.CharField(blank=True, max_length=255)),
      (
       b'user_id', models.IntegerField(db_index=True, null=True)),
      (
       b'username', models.CharField(blank=True, db_index=True, max_length=255)),
      (
       b'object_name', models.CharField(blank=True, db_index=True, max_length=255)),
      (
       b'object_id', models.IntegerField(db_index=True, null=True)),
      (
       b'object_data', models.TextField(blank=True)),
      (
       b'extra', models.TextField(blank=True)),
      (
       b'dc', models.DateTimeField(auto_now_add=True))])]