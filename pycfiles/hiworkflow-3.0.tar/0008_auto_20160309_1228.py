# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hasher/apps/workflow/workflowapp/migrations/0008_auto_20160309_1228.py
# Compiled at: 2016-03-09 07:56:03
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('workflowapp', '0007_auto_20160309_1223')]
    operations = [
     migrations.AlterField(model_name=b'permission', name=b'allow_access', field=models.CharField(max_length=300, null=True)),
     migrations.AlterField(model_name=b'permission', name=b'deny_access', field=models.CharField(max_length=300, null=True))]