# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_sugarcrm/migrations/0010_crm_instance_url.py
# Compiled at: 2016-09-28 11:51:43
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('nodeconductor_sugarcrm', '0009_remove_crm_size_field')]
    operations = [
     migrations.AddField(model_name=b'crm', name=b'instance_url', field=models.URLField(help_text=b'CRMs OpenStack instance URL in NC.', blank=True), preserve_default=True),
     migrations.AlterField(model_name=b'crm', name=b'api_url', field=models.CharField(help_text=b'CRMs OpenStack instance access URL.', max_length=127), preserve_default=True)]