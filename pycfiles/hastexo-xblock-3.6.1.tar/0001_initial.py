# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/florian/git/hastexo-xblock/hastexo/migrations/0001_initial.py
# Compiled at: 2018-08-27 03:02:23
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Stack', fields=[
      (
       b'id',
       models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=64, db_index=True)),
      (
       b'student_id', models.CharField(max_length=40, db_index=True)),
      (
       b'course_id', models.CharField(max_length=50, db_index=True)),
      (
       b'provider', models.CharField(max_length=32)),
      (
       b'protocol', models.CharField(max_length=32)),
      (
       b'port', models.IntegerField(null=True)),
      (
       b'status', models.CharField(max_length=32, db_index=True)),
      (
       b'error_msg', models.CharField(max_length=256)),
      (
       b'ip', models.GenericIPAddressField(null=True)),
      (
       b'user', models.CharField(max_length=32)),
      (
       b'key', models.TextField()),
      (
       b'password', models.CharField(max_length=128)),
      (
       b'launch_task_id', models.CharField(max_length=40)),
      (
       b'launch_timestamp',
       models.DateTimeField(null=True, db_index=True)),
      (
       b'suspend_timestamp',
       models.DateTimeField(null=True, db_index=True)),
      (
       b'created_on',
       models.DateTimeField(auto_now_add=True, db_index=True))]),
     migrations.AlterUniqueTogether(name=b'stack', unique_together=set([('student_id', 'course_id', 'name')]))]