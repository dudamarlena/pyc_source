# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hansek/projects/django_groups_sync/groups_sync/apps.py
# Compiled at: 2020-03-29 08:22:51
# Size of source mod 2**32: 285 bytes
from django.apps import AppConfig

class GroupsSyncConfig(AppConfig):
    name = 'groups_sync'

    def ready(self):
        from django.conf import settings
        settings = settings._wrapped.__dict__
        settings.setdefault('GROUP_SYNC_FILENAME', 'groups_permissions.json')