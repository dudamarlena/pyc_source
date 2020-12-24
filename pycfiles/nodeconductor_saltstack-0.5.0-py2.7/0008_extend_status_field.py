# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/sharepoint/migrations/0008_extend_status_field.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('sharepoint', '0007_site_collection_fields')]
    operations = [
     migrations.AlterField(model_name=b'sharepointtenant', name=b'initialization_status', field=models.CharField(default=b'Not initialized', max_length=30, choices=[('Not initialized', 'Not initialized'), ('Initializing', 'Initializing'), ('Initialized', 'Initialized'), ('Initialization failed', 'Initialization failed')]), preserve_default=True)]