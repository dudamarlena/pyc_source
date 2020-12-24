# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hasher/apps/workflow/workflowapp/migrations/0004_auto_20160308_0952.py
# Compiled at: 2016-03-08 04:52:48
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('workflowapp', '0003_auto_20160308_0709')]
    operations = [
     migrations.AddField(model_name=b'precondition', name=b'filename', field=models.CharField(max_length=300, null=True)),
     migrations.AddField(model_name=b'trigger', name=b'filename', field=models.CharField(max_length=300, null=True)),
     migrations.AlterField(model_name=b'precondition', name=b'condition', field=models.CharField(max_length=300, null=True))]