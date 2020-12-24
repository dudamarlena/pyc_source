# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/sharepoint/migrations/0010__site_collection_types_user_fields.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('sharepoint', '0009_tenant_fields')]
    operations = [
     migrations.AddField(model_name=b'sitecollection', name=b'type', field=models.CharField(default=b'regular', max_length=30, choices=[('main', 'main'), ('admin', 'admin'), ('personal', 'personal'), ('regular', 'regular')]), preserve_default=True),
     migrations.AddField(model_name=b'user', name=b'personal_site_collection', field=models.ForeignKey(related_name=b'+', blank=True, to=b'sharepoint.SiteCollection', null=True), preserve_default=True),
     migrations.AddField(model_name=b'user', name=b'phone', field=models.CharField(max_length=255, blank=True), preserve_default=True)]