# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_zabbix/migrations/0001_squashed_0007_add_sla.py
# Compiled at: 2016-09-21 16:06:28
from __future__ import unicode_literals
from django.db import migrations, models
import nodeconductor.core.models, django_fsm, jsonfield.fields, django.db.models.deletion, django.utils.timezone, nodeconductor.logging.loggers, nodeconductor.core.fields, taggit.managers, model_utils.fields, nodeconductor.core.validators

class Migration(migrations.Migration):
    replaces = [
     ('nodeconductor_zabbix', '0001_initial'), ('nodeconductor_zabbix', '0002_add_error_message'), ('nodeconductor_zabbix', '0003_resource_error_message'), ('nodeconductor_zabbix', '0004_host_tags'), ('nodeconductor_zabbix', '0005_templates_and_items'), ('nodeconductor_zabbix', '0006_extend_items'), ('nodeconductor_zabbix', '0007_add_sla')]
    dependencies = [
     ('taggit', '0002_auto_20150616_2121'),
     ('contenttypes', '0001_initial'),
     ('structure', '0025_add_zabbix_to_settings')]
    operations = [
     migrations.CreateModel(name=b'ZabbixService', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=150, verbose_name=b'name', validators=[nodeconductor.core.validators.validate_name])),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'settings', models.ForeignKey(to=b'structure.ServiceSettings')),
      (
       b'customer', models.ForeignKey(to=b'structure.Customer')),
      (
       b'available_for_all', models.BooleanField(default=False, help_text=b'Service will be automatically added to all customers projects if it is available for all'))], options={b'abstract': False}, bases=(
      nodeconductor.core.models.SerializableAbstractMixin, nodeconductor.logging.loggers.LoggableMixin, models.Model)),
     migrations.CreateModel(name=b'ZabbixServiceProjectLink', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'state', django_fsm.FSMIntegerField(default=5, choices=[(0, 'New'), (5, 'Creation Scheduled'), (6, 'Creating'), (1, 'Sync Scheduled'), (2, 'Syncing'), (3, 'In Sync'), (4, 'Erred')])),
      (
       b'project', models.ForeignKey(to=b'structure.Project')),
      (
       b'service', models.ForeignKey(to=b'nodeconductor_zabbix.ZabbixService')),
      (
       b'error_message', models.TextField(blank=True))], bases=(
      nodeconductor.core.models.SerializableAbstractMixin, nodeconductor.core.models.DescendantMixin, nodeconductor.logging.loggers.LoggableMixin, models.Model)),
     migrations.AlterUniqueTogether(name=b'zabbixservice', unique_together=set([('customer', 'settings')])),
     migrations.AlterUniqueTogether(name=b'zabbixserviceprojectlink', unique_together=set([('service', 'project')])),
     migrations.AddField(model_name=b'zabbixservice', name=b'projects', field=models.ManyToManyField(related_name=b'zabbix_services', through=b'nodeconductor_zabbix.ZabbixServiceProjectLink', to=b'structure.Project')),
     migrations.CreateModel(name=b'Template', fields=[
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
     migrations.AlterUniqueTogether(name=b'template', unique_together=set([('settings', 'backend_id')])),
     migrations.CreateModel(name=b'Host', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=b'created', editable=False)),
      (
       b'modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=b'modified', editable=False)),
      (
       b'description', models.CharField(max_length=500, verbose_name=b'description', blank=True)),
      (
       b'name', models.CharField(max_length=64, verbose_name=b'name', validators=[nodeconductor.core.validators.validate_name])),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'backend_id', models.CharField(max_length=255, blank=True)),
      (
       b'start_time', models.DateTimeField(null=True, blank=True)),
      (
       b'state', django_fsm.FSMIntegerField(default=1, help_text=b'WARNING! Should not be changed manually unless you really know what you are doing.', choices=[(1, 'Provisioning Scheduled'), (2, 'Provisioning'), (3, 'Online'), (4, 'Offline'), (5, 'Starting Scheduled'), (6, 'Starting'), (7, 'Stopping Scheduled'), (8, 'Stopping'), (9, 'Erred'), (10, 'Deletion Scheduled'), (11, 'Deleting'), (13, 'Resizing Scheduled'), (14, 'Resizing'), (15, 'Restarting Scheduled'), (16, 'Restarting')])),
      (
       b'visible_name', models.CharField(max_length=64, verbose_name=b'visible name')),
      (
       b'interface_parameters', jsonfield.fields.JSONField(blank=True)),
      (
       b'host_group_name', models.CharField(max_length=64, verbose_name=b'host group name', blank=True)),
      (
       b'object_id', models.PositiveIntegerField(null=True)),
      (
       b'content_type', models.ForeignKey(to=b'contenttypes.ContentType', null=True)),
      (
       b'service_project_link', models.ForeignKey(related_name=b'hosts', on_delete=django.db.models.deletion.PROTECT, to=b'nodeconductor_zabbix.ZabbixServiceProjectLink')),
      (
       b'error_message', models.TextField(blank=True)),
      (
       b'tags', taggit.managers.TaggableManager(to=b'taggit.Tag', through=b'taggit.TaggedItem', blank=True, help_text=b'A comma-separated list of tags.', verbose_name=b'Tags')),
      (
       b'templates', models.ManyToManyField(related_name=b'hosts', to=b'nodeconductor_zabbix.Template')),
      (
       b'agreed_sla', models.DecimalField(null=True, max_digits=6, decimal_places=4, blank=True)),
      (
       b'service_id', models.CharField(max_length=255, blank=True)),
      (
       b'trigger_id', models.CharField(max_length=255, blank=True))], options={b'abstract': False}, bases=(
      nodeconductor.core.models.SerializableAbstractMixin, nodeconductor.core.models.DescendantMixin, nodeconductor.logging.loggers.LoggableMixin, models.Model)),
     migrations.CreateModel(name=b'Item', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=64)),
      (
       b'template', models.ForeignKey(related_name=b'items', to=b'nodeconductor_zabbix.Template')),
      (
       b'backend_id', models.CharField(max_length=64)),
      (
       b'delay', models.IntegerField()),
      (
       b'history', models.IntegerField()),
      (
       b'units', models.CharField(max_length=255)),
      (
       b'value_type', models.IntegerField(choices=[(0, 'Numeric (float)'), (1, 'Character'), (2, 'Log'), (3, 'Numeric (unsigned)'), (4, 'Text')]))]),
     migrations.CreateModel(name=b'SlaHistory', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'period', models.CharField(max_length=10)),
      (
       b'value', models.DecimalField(null=True, max_digits=11, decimal_places=4, blank=True)),
      (
       b'host', models.ForeignKey(to=b'nodeconductor_zabbix.Host'))], options={b'verbose_name': b'SLA history', 
        b'verbose_name_plural': b'SLA histories'}),
     migrations.CreateModel(name=b'SlaHistoryEvent', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'timestamp', models.IntegerField()),
      (
       b'state', models.CharField(max_length=1, choices=[('U', 'DOWN'), ('D', 'UP')])),
      (
       b'history', models.ForeignKey(related_name=b'events', to=b'nodeconductor_zabbix.SlaHistory'))]),
     migrations.AlterUniqueTogether(name=b'slahistory', unique_together=set([('host', 'period')]))]