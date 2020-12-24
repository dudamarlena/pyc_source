# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hasher/apps/workflow/workflowapp/migrations/0010_state_is_automated.py
# Compiled at: 2016-03-10 08:51:53
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('workflowapp', '0009_auto_20160310_1331')]
    operations = [
     migrations.AddField(model_name=b'state', name=b'is_automated', field=models.BooleanField(default=False))]