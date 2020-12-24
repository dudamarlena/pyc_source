# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/florian/git/hastexo-xblock/hastexo/migrations/0002_stacklog.py
# Compiled at: 2019-08-19 03:16:13
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('hastexo', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'StackLog', fields=[
      (
       b'id',
       models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=64, db_index=True)),
      (
       b'student_id',
       models.CharField(max_length=40, db_index=True)),
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
       b'launch_task_id', models.CharField(max_length=40)),
      (
       b'launch_timestamp',
       models.DateTimeField(null=True, db_index=True)),
      (
       b'suspend_timestamp',
       models.DateTimeField(null=True, db_index=True)),
      (
       b'created_on',
       models.DateTimeField(auto_now_add=True, db_index=True)),
      (
       b'stack',
       models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=b'hastexo.Stack', null=True))], options={b'abstract': False})]