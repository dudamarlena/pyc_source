# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/events/migrations/0005_auto_20160603_1347.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 580 bytes
from django.db import migrations

def event_group_to_groups(apps, schema_editor):
    """
        Migrate event.group foreignkey relationship to the
        many-to-many relationship in event.groups
    """
    Event = apps.get_model('events', 'Event')
    for event in Event.objects.all():
        if event.group:
            event.groups.add(event.group)


class Migration(migrations.Migration):
    dependencies = [
     ('events', '0004_auto_20160603_1347')]
    operations = [
     migrations.RunPython(event_group_to_groups)]