# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/sharepoint/migrations/0001_initial.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations
import django.utils.timezone, django_fsm, nodeconductor.core.models, nodeconductor.core.validators, django.db.models.deletion, nodeconductor.logging.loggers, nodeconductor.core.fields, model_utils.fields

class Migration(migrations.Migration):
    dependencies = [
     ('saltstack', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'Site', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=b'created', editable=False)),
      (
       b'modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=b'modified', editable=False)),
      (
       b'description', models.CharField(max_length=500, verbose_name=b'description', blank=True)),
      (
       b'name', models.CharField(max_length=150, verbose_name=b'name', validators=[nodeconductor.core.validators.validate_name])),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'error_message', models.TextField(blank=True)),
      (
       b'billing_backend_id', models.CharField(help_text=b'ID of a resource in backend', max_length=255, blank=True)),
      (
       b'last_usage_update_time', models.DateTimeField(null=True, blank=True)),
      (
       b'backend_id', models.CharField(max_length=255, blank=True)),
      (
       b'start_time', models.DateTimeField(null=True, blank=True)),
      (
       b'state', django_fsm.FSMIntegerField(default=1, help_text=b'WARNING! Should not be changed manually unless you really know what you are doing.', choices=[(1, 'Provisioning Scheduled'), (2, 'Provisioning'), (3, 'Online'), (4, 'Offline'), (5, 'Starting Scheduled'), (6, 'Starting'), (7, 'Stopping Scheduled'), (8, 'Stopping'), (9, 'Erred'), (10, 'Deletion Scheduled'), (11, 'Deleting'), (13, 'Resizing Scheduled'), (14, 'Resizing'), (15, 'Restarting Scheduled'), (16, 'Restarting')])),
      (
       b'service_project_link', models.ForeignKey(related_name=b'sharepoint_tenants', on_delete=django.db.models.deletion.PROTECT, to=b'saltstack.SaltStackServiceProjectLink'))], options={b'abstract': False}, bases=(
      nodeconductor.core.models.SerializableAbstractMixin, nodeconductor.core.models.DescendantMixin, nodeconductor.logging.loggers.LoggableMixin, models.Model))]