# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idohyeon/Projects/motty/motty/app/migrations/0001_initial.py
# Compiled at: 2017-11-17 03:58:38
# Size of source mod 2**32: 1488 bytes
from __future__ import unicode_literals
import datetime
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Action',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=30)),
      (
       'url', models.CharField(max_length=50)),
      (
       'method', models.CharField(max_length=50)),
      (
       'contentType', models.CharField(max_length=100)),
      (
       'body', models.TextField()),
      (
       'created_at', models.DateTimeField(default=(datetime.datetime(2017, 11, 17, 8, 58, 37, 690997))))]),
     migrations.CreateModel(name='Resource',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=30)),
      (
       'url', models.CharField(max_length=50))]),
     migrations.AddField(model_name='action',
       name='resource',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='app.Resource'))]