# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/liveblog/signals.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 405 bytes
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from .models import LiveBlogEntry
from .tasks import firebase_update_timestamp

@receiver([post_save, pre_delete], sender=LiveBlogEntry)
def update_entry(sender, instance, *args, **kwargs):
    """
    Notify Firebase with updated timestamp
    """
    firebase_update_timestamp.delay(instance.liveblog_id)