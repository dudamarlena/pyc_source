# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/sharepoint/migrations/0004_sharepointtenant_storage_size.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('sharepoint', '0003_new_models')]
    operations = [
     migrations.AddField(model_name=b'sharepointtenant', name=b'storage_size', field=models.PositiveIntegerField(default=1, help_text=b'Maximum size of tenants, MB'), preserve_default=False)]