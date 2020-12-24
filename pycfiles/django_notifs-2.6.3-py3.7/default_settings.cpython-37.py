# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifications/default_settings.py
# Compiled at: 2019-02-21 19:34:58
# Size of source mod 2**32: 581 bytes
"""Default settings for django-notifs project."""
from django.conf import settings
NOTIFICATIONS_PAGINATE_BY = getattr(settings, 'NOTIFICATIONS_PAGINATE_BY', 15)
NOTIFICATIONS_USE_WEBSOCKET = getattr(settings, 'NOTIFICATIONS_USE_WEBSOCKET', False)
NOTIFICATIONS_RABBIT_MQ_URL = getattr(settings, 'NOTIFICATIONS_RABBIT_MQ_URL', 'amqp://guest:guest@localhost:5672')
NOTIFICATIONS_CHANNELS = getattr(settings, 'NOTIFICATIONS_CHANNELS', {})
if NOTIFICATIONS_USE_WEBSOCKET:
    NOTIFICATIONS_CHANNELS['websocket'] = 'notifications.channels.BasicWebSocketChannel'