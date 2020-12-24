# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_sugarcrm/migrations/0012_remove_spl_state.py
# Compiled at: 2016-09-28 11:51:43
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('nodeconductor_sugarcrm', '0011_crm_publishing_state')]
    operations = [
     migrations.RemoveField(model_name=b'sugarcrmserviceprojectlink', name=b'error_message'),
     migrations.RemoveField(model_name=b'sugarcrmserviceprojectlink', name=b'state')]