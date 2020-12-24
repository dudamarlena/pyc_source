# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_jira/migrations/0002_more_issue_fields.py
# Compiled at: 2016-09-16 10:02:59
from __future__ import unicode_literals
from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     ('nodeconductor_jira', '0001_initial')]
    operations = [
     migrations.RemoveField(model_name=b'jiraserviceprojectlink', name=b'error_message'),
     migrations.RemoveField(model_name=b'jiraserviceprojectlink', name=b'state'),
     migrations.AddField(model_name=b'issue', name=b'resolution', field=models.CharField(default=b'', blank=True, max_length=255), preserve_default=False),
     migrations.AddField(model_name=b'issue', name=b'status', field=models.CharField(default=b'', max_length=255), preserve_default=False),
     migrations.AlterField(model_name=b'comment', name=b'user', field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
     migrations.AlterField(model_name=b'issue', name=b'user', field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True))]