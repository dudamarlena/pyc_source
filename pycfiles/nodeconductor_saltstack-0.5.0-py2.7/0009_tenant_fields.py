# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/sharepoint/migrations/0009_tenant_fields.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('sharepoint', '0008_extend_status_field')]
    operations = [
     migrations.RemoveField(model_name=b'sharepointtenant', name=b'initialization_status'),
     migrations.RemoveField(model_name=b'sharepointtenant', name=b'personal_site_collection'),
     migrations.AddField(model_name=b'sharepointtenant', name=b'admin', field=models.ForeignKey(related_name=b'+', blank=True, to=b'sharepoint.User', null=True), preserve_default=True)]