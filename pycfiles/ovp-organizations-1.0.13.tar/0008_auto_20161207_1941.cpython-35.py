# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/migrations/0008_auto_20161207_1941.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 850 bytes
from __future__ import unicode_literals
from django.db import migrations
from ovp_organizations.models import Organization

def add_members(apps, schema_editor):
    for organization in Organization.objects.only('pk', 'members', 'name', 'published', 'deleted', 'owner').all():
        organization.members.add(organization.owner)


def remove_members(apps, schema_editor):
    for organization in Organization.objects.only('pk', 'members', 'name', 'published', 'deleted', 'owner').all():
        organization.members.clear()


class Migration(migrations.Migration):
    dependencies = [
     ('ovp_organizations', '0007_organization_members')]
    operations = [
     migrations.RunPython(add_members, reverse_code=remove_members)]