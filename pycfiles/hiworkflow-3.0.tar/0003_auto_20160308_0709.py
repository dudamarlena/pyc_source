# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hasher/apps/workflow/workflowapp/migrations/0003_auto_20160308_0709.py
# Compiled at: 2016-03-08 02:09:28
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('workflowapp', '0002_trigger')]
    operations = [
     migrations.RenameModel(old_name=b'Stateconnect', new_name=b'Transition')]