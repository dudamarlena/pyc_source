# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/florian/git/hastexo-xblock/hastexo/migrations/0001_initial.py
# Compiled at: 2018-08-27 03:02:23
# Size of source mod 2**32: 1900 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name='Stack',
       fields=[
      (
       'id',
       models.AutoField(verbose_name='ID', serialize=False, auto_created=True,
         primary_key=True)),
      (
       'name', models.CharField(max_length=64, db_index=True)),
      (
       'student_id', models.CharField(max_length=40, db_index=True)),
      (
       'course_id', models.CharField(max_length=50, db_index=True)),
      (
       'provider', models.CharField(max_length=32)),
      (
       'protocol', models.CharField(max_length=32)),
      (
       'port', models.IntegerField(null=True)),
      (
       'status', models.CharField(max_length=32, db_index=True)),
      (
       'error_msg', models.CharField(max_length=256)),
      (
       'ip', models.GenericIPAddressField(null=True)),
      (
       'user', models.CharField(max_length=32)),
      (
       'key', models.TextField()),
      (
       'password', models.CharField(max_length=128)),
      (
       'launch_task_id', models.CharField(max_length=40)),
      (
       'launch_timestamp',
       models.DateTimeField(null=True, db_index=True)),
      (
       'suspend_timestamp',
       models.DateTimeField(null=True, db_index=True)),
      (
       'created_on',
       models.DateTimeField(auto_now_add=True, db_index=True))]),
     migrations.AlterUniqueTogether(name='stack',
       unique_together=(set([('student_id', 'course_id', 'name')])))]