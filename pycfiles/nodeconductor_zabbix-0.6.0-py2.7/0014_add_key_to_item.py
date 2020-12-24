# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_zabbix/migrations/0014_add_key_to_item.py
# Compiled at: 2016-09-21 16:06:28
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('nodeconductor_zabbix', '0013_host_status_and_error')]
    operations = [
     migrations.RenameField(model_name=b'item', old_name=b'name', new_name=b'key'),
     migrations.AddField(model_name=b'item', name=b'name', field=models.CharField(default=b'item', max_length=255), preserve_default=False)]