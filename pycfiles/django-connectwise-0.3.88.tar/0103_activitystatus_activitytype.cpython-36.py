# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0103_activitystatus_activitytype.py
# Compiled at: 2019-08-14 13:00:26
# Size of source mod 2**32: 2178 bytes
from django.db import migrations, models
import django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0102_auto_20190719_1058')]
    operations = [
     migrations.CreateModel(name='ActivityStatus',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'name', models.CharField(max_length=50)),
      (
       'default_flag', models.BooleanField(default=False)),
      (
       'inactive_flag', models.BooleanField(default=False)),
      (
       'spawn_followup_flag', models.BooleanField(default=False)),
      (
       'closed_flag', models.BooleanField(default=False))],
       options={'ordering': ('name', )}),
     migrations.CreateModel(name='ActivityType',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'name', models.CharField(max_length=50)),
      (
       'points', models.IntegerField()),
      (
       'default_flag', models.BooleanField(default=False)),
      (
       'inactive_flag', models.BooleanField(default=False)),
      (
       'email_flag', models.BooleanField(default=False)),
      (
       'memo_flag', models.BooleanField(default=False)),
      (
       'history_flag', models.BooleanField(default=False))],
       options={'ordering': ('name', )})]