# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/sharepoint/migrations/0012_remove_payable_mixin.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('sharepoint', '0011_sharepointtenant_publishing_state')]
    operations = [
     migrations.RemoveField(model_name=b'sharepointtenant', name=b'billing_backend_id'),
     migrations.RemoveField(model_name=b'sharepointtenant', name=b'last_usage_update_time')]