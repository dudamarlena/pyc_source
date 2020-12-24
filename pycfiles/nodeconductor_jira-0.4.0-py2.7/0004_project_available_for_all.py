# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_jira/migrations/0004_project_available_for_all.py
# Compiled at: 2016-09-16 10:02:59
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('nodeconductor_jira', '0003_add_issue_fields')]
    operations = [
     migrations.AddField(model_name=b'project', name=b'available_for_all', field=models.BooleanField(default=False, help_text=b'Allow access to any user'))]