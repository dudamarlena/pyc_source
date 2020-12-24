# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_zabbix/migrations/0010_remove_spl_state.py
# Compiled at: 2016-09-21 16:06:28
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('nodeconductor_zabbix', '0009_itservices_as_resource')]
    operations = [
     migrations.RemoveField(model_name=b'zabbixserviceprojectlink', name=b'error_message'),
     migrations.RemoveField(model_name=b'zabbixserviceprojectlink', name=b'state')]