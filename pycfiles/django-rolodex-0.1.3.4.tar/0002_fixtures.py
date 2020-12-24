# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jon/DMN/Scripts/django-rolodex/rolodex/migrations/0002_fixtures.py
# Compiled at: 2015-01-27 11:13:35
from __future__ import unicode_literals
from django.db import models, migrations
from django.conf import settings

def initial_data(apps, schema_editor):
    if settings.DATABASES.has_key(b'rolodex'):
        if not schema_editor.connection.alias == b'rolodex':
            return
    elif not schema_editor.connection.alias == b'default':
        return
    P2Org_Type = apps.get_model(b'rolodex', b'P2Org_Type')
    P2Org_Type.objects.get_or_create(slug=b'employment', relationship_type=b'employment')
    OrgContactRole = apps.get_model(b'rolodex', b'OrgContactRole')
    OrgContactRole.objects.get_or_create(slug=b'public-records-contact', role=b'public records contact', description=b'A contact to receive public records requests.')
    PersonRole = apps.get_model(b'rolodex', b'PersonRole')
    PersonRole.objects.get_or_create(slug=b'public-information-officer', role=b'public information officer', description=b'A person responsible for fielding public records requests.')


class Migration(migrations.Migration):
    dependencies = [
     ('rolodex', '0001_initial')]
    operations = [
     migrations.RunPython(initial_data)]