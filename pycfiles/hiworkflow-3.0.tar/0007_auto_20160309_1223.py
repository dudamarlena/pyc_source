# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hasher/apps/workflow/workflowapp/migrations/0007_auto_20160309_1223.py
# Compiled at: 2016-03-09 07:56:03
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('workflowapp', '0006_assignee_assigned_by')]
    operations = [
     migrations.AlterField(model_name=b'permission', name=b'allow_access', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
     migrations.AlterField(model_name=b'permission', name=b'deny_access', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'deny_access_user', to=settings.AUTH_USER_MODEL))]