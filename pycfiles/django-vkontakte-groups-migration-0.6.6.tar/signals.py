# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramusus/workspace/manufacture/env/src/django-vkontakte-groups-migration/vkontakte_groups_migration/signals.py
# Compiled at: 2014-05-11 12:55:49
from django.dispatch import Signal
from django.conf import settings
from annoying.decorators import signals
from vkontakte_groups.models import Group
from models import GroupMigration, update_group_users
group_migration_updated = Signal(providing_args=['instance'])
group_users_updated = Signal(providing_args=['instance'])

@signals(group_migration_updated, sender=GroupMigration)
def group_users_update_m2m(sender, instance, **kwargs):
    if 'djcelery' in settings.INSTALLED_APPS:
        from tasks import VkontakteGroupUpdateUsersM2M
        return VkontakteGroupUpdateUsersM2M.delay(instance.id)
    update_group_users(instance.group)