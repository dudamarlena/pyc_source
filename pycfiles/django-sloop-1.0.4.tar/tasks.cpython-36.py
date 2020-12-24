# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/django_sloop/tasks.py
# Compiled at: 2019-08-14 11:46:19
# Size of source mod 2**32: 878 bytes
from celery import shared_task
from .utils import get_device_model

@shared_task()
def send_push_notification(device_id, message, url, badge_count, sound, extra, category, **kwargs):
    """
    Sends a push notification message to the specified tokens
    """
    device_model = get_device_model()
    device = device_model.objects.get(id=device_id)
    (device.send_push_notification)(message, url, badge_count, sound, extra, category, **kwargs)
    return 'Message: %s' % message


@shared_task()
def send_silent_push_notification(device_id, extra, badge_count, content_available, **kwargs):
    """
    Sends a push notification message to the specified tokens
    """
    device_model = get_device_model()
    device = device_model.objects.get(id=device_id)
    (device.send_silent_push_notification)(extra, badge_count, content_available, **kwargs)
    return 'Silent push'