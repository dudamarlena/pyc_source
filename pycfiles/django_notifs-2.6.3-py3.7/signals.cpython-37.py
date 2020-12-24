# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifications/signals.py
# Compiled at: 2019-08-12 19:23:41
# Size of source mod 2**32: 1845 bytes
"""Defines and listens to notification signals."""
import warnings
from django.dispatch import Signal, receiver
from . import NotificationError
from .models import Notification
from .tasks import send_notification
notify = Signal(providing_args=('source', 'source_display_name', 'recipient', 'action',
                                'categoryobj', 'url', 'short_description', 'extra_data',
                                'silent', 'channels'))
read = Signal(providing_args=('notify_id', 'recipient'))

@receiver(notify)
def create_notification(**kwargs):
    """Notify signal receiver."""
    warnings.warn("The 'notify' Signal will be removed in 2.6.5 Please use the helper functions in notifications.utils", PendingDeprecationWarning)
    params = kwargs.copy()
    del params['signal']
    del params['sender']
    try:
        del params['silent']
    except KeyError:
        pass

    notification = Notification(**params)
    if not kwargs.get('silent', False):
        notification.save()
    send_notification.delay(notification.to_json())


@receiver(read)
def read_notification(**kwargs):
    """
    Mark notification as read.

    Raises NotificationError if the user doesn't have access
    to read the notification
    """
    warnings.warn("The 'read' Signal will be removed in 2.6.5 Please use the helper functions in notifications.utils", PendingDeprecationWarning)
    notify_id = kwargs['notify_id']
    recipient = kwargs['recipient']
    notification = Notification.objects.get(id=notify_id)
    if recipient != notification.recipient:
        raise NotificationError('You cannot read this notification')
    notification.read()