# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/sharepoint/migrations/0007_site_collection_fields.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('sharepoint', '0006_site_collections')]
    operations = [
     migrations.RenameField(model_name=b'sharepointtenant', old_name=b'users_site_collection', new_name=b'personal_site_collection'),
     migrations.AlterField(model_name=b'sitecollection', name=b'access_url', field=models.CharField(max_length=255), preserve_default=True),
     migrations.AlterField(model_name=b'sitecollection', name=b'site_url', field=models.CharField(max_length=255, blank=True), preserve_default=True),
     migrations.AlterField(model_name=b'sitecollection', name=b'template', field=models.ForeignKey(related_name=b'site_collections', blank=True, to=b'sharepoint.Template', null=True), preserve_default=True)]