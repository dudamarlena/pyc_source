# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifications/apps.py
# Compiled at: 2019-08-12 19:31:45
# Size of source mod 2**32: 235 bytes
"""Register all Signals."""
from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    __doc__ = 'App Config.'
    name = 'notifications'

    def ready(self):
        """Import signals."""
        from . import signals