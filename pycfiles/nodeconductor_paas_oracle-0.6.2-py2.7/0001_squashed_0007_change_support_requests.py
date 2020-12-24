# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_paas_oracle/migrations/0001_squashed_0007_change_support_requests.py
# Compiled at: 2016-12-16 07:39:01
from __future__ import unicode_literals
from django.db import migrations, models
import taggit.managers, nodeconductor.logging.loggers, django_fsm, nodeconductor.core.models, django.db.models.deletion, django.utils.timezone, nodeconductor.core.fields, django.core.validators, model_utils.fields, nodeconductor.core.validators

class Migration(migrations.Migration):
    replaces = [
     ('nodeconductor_paas_oracle', '0001_initial'), ('nodeconductor_paas_oracle', '0002_flavor'), ('nodeconductor_paas_oracle', '0003_db_type_choices'), ('nodeconductor_paas_oracle', '0004_remove_flavor_backend_id'), ('nodeconductor_paas_oracle', '0005_add_db_arch_size'), ('nodeconductor_paas_oracle', '0006_add_ssh_metadata'), ('nodeconductor_paas_oracle', '0007_change_support_requests')]
    dependencies = [
     ('structure', '0035_settings_tags_and_scope'),
     ('taggit', '0002_auto_20150616_2121'),
     ('openstack', '0001_initial'),
     ('nodeconductor_jira', '0004_project_available_for_all')]
    operations = [
     migrations.CreateModel(name=b'Deployment', fields=[
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
       b'state', django_fsm.FSMIntegerField(default=1, help_text=b'WARNING! Should not be changed manually unless you really know what you are doing.', choices=[(1, 'Provisioning Scheduled'), (2, 'Provisioning'), (3, 'Online'), (4, 'Offline'), (5, 'Starting Scheduled'), (6, 'Starting'), (7, 'Stopping Scheduled'), (8, 'Stopping'), (9, 'Erred'), (10, 'Deletion Scheduled'), (11, 'Deleting'), (13, 'Resizing Scheduled'), (14, 'Resizing'), (15, 'Restarting Scheduled'), (16, 'Restarting')])),
      (
       b'backend_id', models.CharField(max_length=255, blank=True)),
      (
       b'start_time', models.DateTimeField(null=True, blank=True)),
      (
       b'report', models.TextField(blank=True)),
      (
       b'db_name', models.CharField(max_length=256)),
      (
       b'db_size', models.PositiveIntegerField(help_text=b'Data storage size in GB', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(2048)])),
      (
       b'db_arch_size', models.PositiveIntegerField(help_text=b'Archive storage size in GB', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(2048)])),
      (
       b'db_type', models.PositiveSmallIntegerField(choices=[(1, 'RAC'), (2, 'Single Instance/ASM'), (3, 'Single Instance')])),
      (
       b'db_version', models.CharField(max_length=256, choices=[('11.2.0.4', '11.2.0.4'), ('12.1.0.2', '12.1.0.2')])),
      (
       b'db_template', models.CharField(max_length=256, choices=[('General Purpose', 'General Purpose'), ('Data Warehouse', 'Data Warehouse')])),
      (
       b'db_charset', models.CharField(max_length=256, choices=[('AL32UTF8 - Unicode UTF-8 Universal Character Set', 'AL32UTF8 - Unicode UTF-8 Universal Character Set'), ('AR8ISO8859P6 - ISO 8859-6 Latin/Arabic', 'AR8ISO8859P6 - ISO 8859-6 Latin/Arabic'), ('AR8MSWIN1256 - MS Windows Code Page 1256 8-Bit Latin/Arabic', 'AR8MSWIN1256 - MS Windows Code Page 1256 8-Bit Latin/Arabic'), ('Other - please specify in Addtional Data field.', 'Other - please specify in Addtional Data field.')])),
      (
       b'user_data', models.TextField(blank=True)),
      (
       b'key_name', models.CharField(max_length=50, blank=True)),
      (
       b'key_fingerprint', models.CharField(max_length=47, blank=True))], options={b'abstract': False}, bases=(
      nodeconductor.core.models.SerializableAbstractMixin, nodeconductor.core.models.DescendantMixin, nodeconductor.logging.loggers.LoggableMixin, models.Model)),
     migrations.CreateModel(name=b'Flavor', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=150, verbose_name=b'name', validators=[nodeconductor.core.validators.validate_name])),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'cores', models.PositiveSmallIntegerField(help_text=b'Number of cores in a VM')),
      (
       b'ram', models.PositiveIntegerField(help_text=b'Memory size in MiB')),
      (
       b'disk', models.PositiveIntegerField(help_text=b'Root disk size in MiB'))], options={b'abstract': False}),
     migrations.CreateModel(name=b'OracleService', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=150, verbose_name=b'name', validators=[nodeconductor.core.validators.validate_name])),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'available_for_all', models.BooleanField(default=False, help_text=b'Service will be automatically added to all customers projects if it is available for all')),
      (
       b'customer', models.ForeignKey(to=b'structure.Customer'))], options={b'abstract': False}, bases=(
      nodeconductor.core.models.SerializableAbstractMixin, nodeconductor.core.models.DescendantMixin, nodeconductor.logging.loggers.LoggableMixin, models.Model)),
     migrations.CreateModel(name=b'OracleServiceProjectLink', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'project', models.ForeignKey(to=b'structure.Project')),
      (
       b'service', models.ForeignKey(to=b'nodeconductor_paas_oracle.OracleService'))], options={b'abstract': False}, bases=(
      nodeconductor.core.models.SerializableAbstractMixin, nodeconductor.core.models.DescendantMixin, nodeconductor.logging.loggers.LoggableMixin, models.Model)),
     migrations.AddField(model_name=b'oracleservice', name=b'projects', field=models.ManyToManyField(related_name=b'oracle_services', through=b'nodeconductor_paas_oracle.OracleServiceProjectLink', to=b'structure.Project')),
     migrations.AddField(model_name=b'oracleservice', name=b'settings', field=models.ForeignKey(to=b'structure.ServiceSettings')),
     migrations.AddField(model_name=b'deployment', name=b'flavor', field=models.ForeignKey(related_name=b'+', to=b'nodeconductor_paas_oracle.Flavor')),
     migrations.AddField(model_name=b'deployment', name=b'service_project_link', field=models.ForeignKey(related_name=b'deployments', on_delete=django.db.models.deletion.PROTECT, to=b'nodeconductor_paas_oracle.OracleServiceProjectLink')),
     migrations.AddField(model_name=b'deployment', name=b'support_requests', field=models.ManyToManyField(related_name=b'_deployment_support_requests_+', to=b'nodeconductor_jira.Issue')),
     migrations.AddField(model_name=b'deployment', name=b'tags', field=taggit.managers.TaggableManager(to=b'taggit.Tag', through=b'taggit.TaggedItem', blank=True, help_text=b'A comma-separated list of tags.', verbose_name=b'Tags')),
     migrations.AddField(model_name=b'deployment', name=b'tenant', field=models.ForeignKey(related_name=b'+', to=b'openstack.Tenant')),
     migrations.AlterUniqueTogether(name=b'oracleserviceprojectlink', unique_together=set([('service', 'project')])),
     migrations.AlterUniqueTogether(name=b'oracleservice', unique_together=set([('customer', 'settings')]))]