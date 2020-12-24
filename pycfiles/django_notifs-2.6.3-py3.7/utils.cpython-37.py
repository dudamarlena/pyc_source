# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifications/utils.py
# Compiled at: 2019-08-12 19:54:52
# Size of source mod 2**32: 870 bytes
"""Utilities and helper functions."""
from . import NotificationError
from .models import Notification
from .tasks import send_notification

def notify(silent=False, **kwargs):
    """Helper method to send a notification."""
    notification = Notification(**kwargs)
    if not silent:
        notification.save()
    send_notification.delay(notification.to_json())


def read(notify_id, recipient):
    """
    Helper method to read a notification.

    Raises NotificationError if the user doesn't have access
    to read the notification
    """
    notification = Notification.objects.get(id=notify_id)
    if recipient != notification.recipient:
        raise NotificationError('You cannot read this notification')
    notification.read()