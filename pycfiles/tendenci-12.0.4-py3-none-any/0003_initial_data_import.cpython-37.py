# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/helpdesk/migrations/0003_initial_data_import.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1069 bytes
import os
from django.db import migrations
from django.core import serializers
fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures'))
fixture_filename = 'emailtemplate.json'

def deserialize_fixture():
    fixture_file = os.path.join(fixture_dir, fixture_filename)
    with open(fixture_file, 'rb') as (fixture):
        return list(serializers.deserialize('json', fixture, ignorenonexistent=True))


def load_fixture(apps, schema_editor):
    objects = deserialize_fixture()
    for obj in objects:
        obj.save()


def unload_fixture(apps, schema_editor):
    """Delete all EmailTemplate objects"""
    objects = deserialize_fixture()
    EmailTemplate = apps.get_model('helpdesk', 'emailtemplate')
    EmailTemplate.objects.filter(pk__in=[obj.object.pk for obj in objects]).delete()


class Migration(migrations.Migration):
    dependencies = [
     ('helpdesk', '0002_populate_usersettings')]
    operations = [
     migrations.RunPython(load_fixture, reverse_code=unload_fixture)]