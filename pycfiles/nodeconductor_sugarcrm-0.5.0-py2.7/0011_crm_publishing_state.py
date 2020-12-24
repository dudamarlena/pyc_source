# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_sugarcrm/migrations/0011_crm_publishing_state.py
# Compiled at: 2016-09-28 11:51:43
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('nodeconductor_sugarcrm', '0010_crm_instance_url')]
    operations = [
     migrations.AddField(model_name=b'crm', name=b'publishing_state', field=models.CharField(default=b'not published', max_length=30, choices=[('not published', 'Not published'), ('published', 'Published'), ('requested', 'Requested')]), preserve_default=True)]