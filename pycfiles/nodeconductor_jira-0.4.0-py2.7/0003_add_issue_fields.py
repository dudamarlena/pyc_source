# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_jira/migrations/0003_add_issue_fields.py
# Compiled at: 2016-09-16 10:02:59
from __future__ import unicode_literals
from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import django.utils.timezone
from django.conf import settings
import django_fsm, nodeconductor.core.fields, model_utils.fields

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('nodeconductor_jira', '0002_more_issue_fields')]
    operations = [
     migrations.CreateModel(name=b'Attachment', fields=[
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
       b'file', models.FileField(upload_to=b'jira_attachments')),
      (
       b'backend_id', models.CharField(max_length=255))], options={b'abstract': False}),
     migrations.AddField(model_name=b'issue', name=b'impact', field=models.SmallIntegerField(default=0, choices=[(0, 'n/a'), (1, 'Small - Partial loss of service, one person affected'), (2, 'Medium - One department or service is affected'), (3, 'Large - Whole organization or all services are affected')])),
     migrations.AddField(model_name=b'issue', name=b'priority', field=models.SmallIntegerField(default=0, choices=[(0, 'n/a'), (1, 'Minor'), (2, 'Major'), (3, 'Critical')])),
     migrations.AddField(model_name=b'issue', name=b'type', field=models.CharField(default=b'Support Request', max_length=255), preserve_default=False),
     migrations.AddField(model_name=b'issue', name=b'updated', field=models.DateTimeField(default=datetime.datetime(2016, 4, 14, 17, 9, 18, 260377, tzinfo=utc), auto_now_add=True), preserve_default=False),
     migrations.AddField(model_name=b'issue', name=b'updated_username', field=models.CharField(max_length=255, blank=True)),
     migrations.AddField(model_name=b'project', name=b'impact_field', field=models.CharField(max_length=64, blank=True)),
     migrations.AddField(model_name=b'attachment', name=b'issue', field=models.ForeignKey(related_name=b'attachments', to=b'nodeconductor_jira.Issue')),
     migrations.AddField(model_name=b'attachment', name=b'user', field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True))]