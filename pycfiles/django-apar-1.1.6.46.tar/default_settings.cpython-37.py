# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/messaging/default_settings.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 466 bytes
"""Default settings for django-notifs project."""
from django.conf import settings
NOTIFICATIONS_PAGINATE_BY = getattr(settings, 'NOTIFICATIONS_PAGINATE_BY', 15)
NOTIFICATIONS_USE_WEBSOCKET = getattr(settings, 'NOTIFICATIONS_USE_WEBSOCKET', False)
NOTIFICATIONS_CHANNELS = getattr(settings, 'NOTIFICATIONS_CHANNELS', {})
if NOTIFICATIONS_USE_WEBSOCKET:
    NOTIFICATIONS_CHANNELS['websocket'] = 'aparnik.contrib.messaging.channels.BasicWebSocketChannel'