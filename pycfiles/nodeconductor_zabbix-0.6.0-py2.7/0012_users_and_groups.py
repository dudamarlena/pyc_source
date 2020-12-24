# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_zabbix/migrations/0012_users_and_groups.py
# Compiled at: 2016-09-21 16:06:28
from __future__ import unicode_literals
from django.db import migrations, models
import nodeconductor.core.fields, django_fsm, nodeconductor.core.validators

class Migration(migrations.Migration):
    dependencies = [
     ('structure', '0034_change_service_settings_state_field'),
     ('nodeconductor_zabbix', '0011_migrate_state_field')]
    operations = [
     migrations.CreateModel(name=b'User', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=150, verbose_name=b'name', validators=[nodeconductor.core.validators.validate_name])),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'error_message', models.TextField(blank=True)),
      (
       b'state', django_fsm.FSMIntegerField(default=5, choices=[(5, 'Creation Scheduled'), (6, 'Creating'), (1, 'Update Scheduled'), (2, 'Updating'), (7, 'Deletion Scheduled'), (8, 'Deleting'), (3, 'OK'), (4, 'Erred')])),
      (
       b'backend_id', models.CharField(max_length=255, db_index=True)),
      (
       b'alias', models.CharField(max_length=150)),
      (
       b'surname', models.CharField(max_length=150)),
      (
       b'type', models.CharField(default=b'1', max_length=30, choices=[('1', 'default'), ('2', 'admin'), ('3', 'superadmin')])),
      (
       b'password', models.CharField(max_length=150, blank=True)),
      (
       b'phone', models.CharField(max_length=30, blank=True))]),
     migrations.CreateModel(name=b'UserGroup', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=150, verbose_name=b'name', validators=[nodeconductor.core.validators.validate_name])),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'backend_id', models.CharField(max_length=255, db_index=True)),
      (
       b'settings', models.ForeignKey(related_name=b'+', to=b'structure.ServiceSettings'))], options={b'abstract': False}),
     migrations.AddField(model_name=b'user', name=b'groups', field=models.ManyToManyField(related_name=b'users', to=b'nodeconductor_zabbix.UserGroup')),
     migrations.AddField(model_name=b'user', name=b'settings', field=models.ForeignKey(related_name=b'+', to=b'structure.ServiceSettings')),
     migrations.AlterUniqueTogether(name=b'usergroup', unique_together=set([('settings', 'backend_id')])),
     migrations.AlterUniqueTogether(name=b'user', unique_together=set([('alias', 'settings')]))]