# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_sugarcrm/migrations/0001_squashed_0009_remove_crm_size_field.py
# Compiled at: 2016-09-28 11:51:43
from __future__ import unicode_literals
from django.db import migrations, models
import taggit.managers, django_fsm, nodeconductor.core.models, django.db.models.deletion, django.utils.timezone, nodeconductor.logging.loggers, nodeconductor.core.fields, django.core.validators, model_utils.fields, nodeconductor.core.validators

class Migration(migrations.Migration):
    replaces = [
     ('nodeconductor_sugarcrm', '0001_initial'), ('nodeconductor_sugarcrm', '0002_add_crm_access_fields'), ('nodeconductor_sugarcrm', '0003_paid_resources'), ('nodeconductor_sugarcrm', '0004_add_error_message'), ('nodeconductor_sugarcrm', '0005_crm_size'), ('nodeconductor_sugarcrm', '0006_resource_error_message'), ('nodeconductor_sugarcrm', '0007_init_user_limit_count_quota'), ('nodeconductor_sugarcrm', '0008_crm_tags'), ('nodeconductor_sugarcrm', '0009_remove_crm_size_field')]
    dependencies = [
     ('taggit', '0002_auto_20150616_2121'),
     ('structure', '0024_add_sugarcrm_to_settings'),
     ('contenttypes', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'SugarCRMService', fields=[
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
       b'available_for_all', models.BooleanField(default=False, help_text=b'Service will be automatically added to all customers projects if it is available for all'))], options={b'abstract': False, 
        b'verbose_name': b'SugarCRM service', 
        b'verbose_name_plural': b'SugarCRM services'}, bases=(
      nodeconductor.core.models.SerializableAbstractMixin, nodeconductor.logging.loggers.LoggableMixin, models.Model)),
     migrations.CreateModel(name=b'SugarCRMServiceProjectLink', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'state', django_fsm.FSMIntegerField(default=5, choices=[(0, 'New'), (5, 'Creation Scheduled'), (6, 'Creating'), (1, 'Sync Scheduled'), (2, 'Syncing'), (3, 'In Sync'), (4, 'Erred')])),
      (
       b'project', models.ForeignKey(to=b'structure.Project')),
      (
       b'service', models.ForeignKey(to=b'nodeconductor_sugarcrm.SugarCRMService')),
      (
       b'error_message', models.TextField(blank=True))], bases=(
      nodeconductor.core.models.SerializableAbstractMixin, nodeconductor.logging.loggers.LoggableMixin, models.Model), options={b'verbose_name': b'SugarCRM service project link', 
        b'verbose_name_plural': b'SugarCRM service project links'}),
     migrations.AlterUniqueTogether(name=b'sugarcrmserviceprojectlink', unique_together=set([('service', 'project')])),
     migrations.AlterUniqueTogether(name=b'sugarcrmservice', unique_together=set([('customer', 'settings')])),
     migrations.AddField(model_name=b'sugarcrmservice', name=b'projects', field=models.ManyToManyField(related_name=b'sugarcrm_services', through=b'nodeconductor_sugarcrm.SugarCRMServiceProjectLink', to=b'structure.Project')),
     migrations.CreateModel(name=b'CRM', fields=[
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
       b'backend_id', models.CharField(max_length=255, blank=True)),
      (
       b'start_time', models.DateTimeField(null=True, blank=True)),
      (
       b'state', django_fsm.FSMIntegerField(default=1, help_text=b'WARNING! Should not be changed manually unless you really know what you are doing.', choices=[(1, 'Provisioning Scheduled'), (2, 'Provisioning'), (3, 'Online'), (4, 'Offline'), (5, 'Starting Scheduled'), (6, 'Starting'), (7, 'Stopping Scheduled'), (8, 'Stopping'), (9, 'Erred'), (10, 'Deletion Scheduled'), (11, 'Deleting'), (13, 'Resizing Scheduled'), (14, 'Resizing'), (15, 'Restarting Scheduled'), (16, 'Restarting')])),
      (
       b'service_project_link', models.ForeignKey(related_name=b'crms', on_delete=django.db.models.deletion.PROTECT, to=b'nodeconductor_sugarcrm.SugarCRMServiceProjectLink')),
      (
       b'error_message', models.TextField(blank=True)),
      (
       b'tags', taggit.managers.TaggableManager(to=b'taggit.Tag', through=b'taggit.TaggedItem', blank=True, help_text=b'A comma-separated list of tags.', verbose_name=b'Tags')),
      (
       b'admin_username', models.CharField(max_length=60)),
      (
       b'admin_password', models.CharField(max_length=255)),
      (
       b'api_url', models.CharField(help_text=b'CRMs OpenStack instance URL', max_length=127)),
      (
       b'billing_backend_id', models.CharField(help_text=b'ID of a resource in backend', max_length=255, blank=True)),
      (
       b'last_usage_update_time', models.DateTimeField(null=True, blank=True))], options={b'abstract': False, 
        b'verbose_name': b'CRM', 
        b'verbose_name_plural': b'CRMs'}, bases=(
      nodeconductor.core.models.SerializableAbstractMixin, nodeconductor.logging.loggers.LoggableMixin, models.Model))]