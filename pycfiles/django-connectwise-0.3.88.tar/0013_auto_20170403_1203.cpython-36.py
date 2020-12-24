# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0013_auto_20170403_1203.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1174 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0012_auto_20170320_1057')]
    operations = [
     migrations.CreateModel(name='CompanyStatus',
       fields=[
      (
       'id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
      (
       'name', models.CharField(max_length=50)),
      (
       'default_flag', models.BooleanField()),
      (
       'inactive_flag', models.BooleanField()),
      (
       'notify_flag', models.BooleanField()),
      (
       'dissalow_saving_flag', models.BooleanField()),
      (
       'notification_message', models.CharField(max_length=500)),
      (
       'custom_note_flag', models.BooleanField()),
      (
       'cancel_open_tracks_flag', models.BooleanField()),
      (
       'track_id', models.PositiveSmallIntegerField(blank=True, null=True))]),
     migrations.RemoveField(model_name='company',
       name='status')]