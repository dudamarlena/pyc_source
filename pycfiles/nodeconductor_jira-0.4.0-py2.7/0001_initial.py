# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_jira/migrations/0001_initial.py
# Compiled at: 2016-09-16 10:02:59
from __future__ import unicode_literals
from django.db import migrations, models
import django_fsm, nodeconductor.core.models, django.db.models.deletion
from django.conf import settings
import django.utils.timezone, nodeconductor.logging.loggers, nodeconductor.core.fields, taggit.managers, model_utils.fields, nodeconductor.core.validators

class Migration(migrations.Migration):
    dependencies = [
     ('taggit', '0002_auto_20150616_2121'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('structure', '0032_make_options_optional')]
    operations = [
     migrations.CreateModel(name=b'Comment', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=b'created', editable=False)),
      (
       b'modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=b'modified', editable=False)),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'error_message', models.TextField(blank=True)),
      (
       b'state', django_fsm.FSMIntegerField(default=5, choices=[(5, 'Creation Scheduled'), (6, 'Creating'), (1, 'Update Scheduled'), (2, 'Updating'), (7, 'Deletion Scheduled'), (8, 'Deleting'), (3, 'OK'), (4, 'Erred')])),
      (
       b'message', models.TextField(blank=True)),
      (
       b'backend_id', models.CharField(max_length=255))], options={b'abstract': False}),
     migrations.CreateModel(name=b'Issue', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=b'created', editable=False)),
      (
       b'modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=b'modified', editable=False)),
      (
       b'uuid', nodeconductor.core.fields.UUIDField()),
      (
       b'error_message', models.TextField(blank=True)),
      (
       b'state', django_fsm.FSMIntegerField(default=5, choices=[(5, 'Creation Scheduled'), (6, 'Creating'), (1, 'Update Scheduled'), (2, 'Updating'), (7, 'Deletion Scheduled'), (8, 'Deleting'), (3, 'OK'), (4, 'Erred')])),
      (
       b'summary', models.CharField(max_length=255)),
      (
       b'description', models.TextField(blank=True)),
      (
       b'backend_id', models.CharField(max_length=255))], options={b'abstract': False}),
     migrations.CreateModel(name=b'JiraService', fields=[
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
     migrations.CreateModel(name=b'JiraServiceProjectLink', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'error_message', models.TextField(blank=True)),
      (
       b'state', django_fsm.FSMIntegerField(default=5, choices=[(0, 'New'), (5, 'Creation Scheduled'), (6, 'Creating'), (1, 'Sync Scheduled'), (2, 'Syncing'), (3, 'In Sync'), (4, 'Erred')]))], options={b'abstract': False}, bases=(
      nodeconductor.core.models.SerializableAbstractMixin, nodeconductor.core.models.DescendantMixin, nodeconductor.logging.loggers.LoggableMixin, models.Model)),
     migrations.CreateModel(name=b'Project', fields=[
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
       b'state', django_fsm.FSMIntegerField(default=5, choices=[(5, 'Creation Scheduled'), (6, 'Creating'), (1, 'Update Scheduled'), (2, 'Updating'), (7, 'Deletion Scheduled'), (8, 'Deleting'), (3, 'OK'), (4, 'Erred')])),
      (
       b'backend_id', models.CharField(max_length=255, blank=True)),
      (
       b'start_time', models.DateTimeField(null=True, blank=True)),
      (
       b'reporter_field', models.CharField(max_length=64, blank=True)),
      (
       b'default_issue_type', models.CharField(max_length=64, blank=True)),
      (
       b'service_project_link', models.ForeignKey(related_name=b'projects', on_delete=django.db.models.deletion.PROTECT, to=b'nodeconductor_jira.JiraServiceProjectLink')),
      (
       b'tags', taggit.managers.TaggableManager(to=b'taggit.Tag', through=b'taggit.TaggedItem', blank=True, help_text=b'A comma-separated list of tags.', verbose_name=b'Tags'))], options={b'abstract': False}, bases=(
      nodeconductor.core.models.SerializableAbstractMixin, nodeconductor.core.models.DescendantMixin, nodeconductor.logging.loggers.LoggableMixin, models.Model)),
     migrations.AddField(model_name=b'jiraserviceprojectlink', name=b'project', field=models.ForeignKey(to=b'structure.Project')),
     migrations.AddField(model_name=b'jiraserviceprojectlink', name=b'service', field=models.ForeignKey(to=b'nodeconductor_jira.JiraService')),
     migrations.AddField(model_name=b'jiraservice', name=b'projects', field=models.ManyToManyField(related_name=b'jira_services', through=b'nodeconductor_jira.JiraServiceProjectLink', to=b'structure.Project')),
     migrations.AddField(model_name=b'jiraservice', name=b'settings', field=models.ForeignKey(to=b'structure.ServiceSettings')),
     migrations.AddField(model_name=b'issue', name=b'project', field=models.ForeignKey(related_name=b'issues', to=b'nodeconductor_jira.Project')),
     migrations.AddField(model_name=b'issue', name=b'user', field=models.ForeignKey(to=settings.AUTH_USER_MODEL)),
     migrations.AddField(model_name=b'comment', name=b'issue', field=models.ForeignKey(related_name=b'comments', to=b'nodeconductor_jira.Issue')),
     migrations.AddField(model_name=b'comment', name=b'user', field=models.ForeignKey(to=settings.AUTH_USER_MODEL)),
     migrations.AlterUniqueTogether(name=b'jiraserviceprojectlink', unique_together=set([('service', 'project')])),
     migrations.AlterUniqueTogether(name=b'jiraservice', unique_together=set([('customer', 'settings')]))]