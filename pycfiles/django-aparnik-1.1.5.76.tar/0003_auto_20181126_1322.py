# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/managements/migrations/0003_auto_20181126_1322.py
# Compiled at: 2018-11-26 06:42:11
from __future__ import unicode_literals
from django.db import migrations

def rename_admin_groups(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Group = apps.get_model(b'auth', b'Group')
    try:
        group = Group.objects.get(pk=1)
        group.name = b'admin'
        group.save()
    except Exception:
        pass


class Migration(migrations.Migration):
    dependencies = [
     ('managements', '0002_auto_20181105_2023')]
    operations = [
     migrations.RunPython(rename_admin_groups, reverse_code=migrations.RunPython.noop)]