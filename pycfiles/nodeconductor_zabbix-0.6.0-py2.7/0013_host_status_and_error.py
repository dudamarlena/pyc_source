# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_zabbix/migrations/0013_host_status_and_error.py
# Compiled at: 2016-09-21 16:06:28
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('nodeconductor_zabbix', '0012_users_and_groups')]
    operations = [
     migrations.AddField(model_name=b'host', name=b'error', field=models.CharField(help_text=b'Error text if Zabbix agent is unavailable.', max_length=500, blank=True)),
     migrations.AddField(model_name=b'host', name=b'status', field=models.CharField(default=b'0', max_length=30, choices=[('0', 'monitored'), ('1', 'unmonitored')]))]