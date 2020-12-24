# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hasher/apps/workflow/workflowapp/migrations/0006_assignee_assigned_by.py
# Compiled at: 2016-03-09 05:39:45
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('workflowapp', '0005_auto_20160308_1403')]
    operations = [
     migrations.AddField(model_name=b'assignee', name=b'assigned_by', field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name=b'assigned_by', to=settings.AUTH_USER_MODEL), preserve_default=False)]