# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifications/models.py
# Compiled at: 2019-02-21 19:36:52
# Size of source mod 2**32: 3360 bytes
"""Notification model."""
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from .fields import JSONField, ListField

class NotificationQuerySet(models.QuerySet):
    __doc__ = 'Notifications QuerySet.'

    def all_unread(self):
        """Return all unread notifications."""
        return self.filter(is_read=False)

    def all_read(self):
        """Return all read notifications."""
        return self.filter(is_read=True)


class Notification(models.Model):
    __doc__ = "\n    Model for notifications.\n\n    Parameters:\n    ----------\n    source: A ForeignKey to Django's User model\n        (Can be null if it's not a User to User Notification)\n\n    source_display_name: A User Friendly name\n        for the source of the notification.\n\n    recipient: The Recipient of the notification.\n        It's a ForeignKey to Django's User model.\n\n    action: Verbal action for the notification\n        E.g Sent, Cancelled, Bought e.t.c\n\n    obj: The id of the object associated with the notification\n        (Can be null)\n\n    short_description: The body of the notification.\n\n    url: The url of the object associated with the notification\n        (Can be null)\n    channels: Channel(s) that were/was used to deliver the message\n\n    extra_data: Extra information that was passed in the notification\n        (Optional but default value is an empty dict {})\n    "
    User = settings.AUTH_USER_MODEL

    class Meta:
        __doc__ = 'Specify ordering for notifications.'
        ordering = ('-id', )

    source = models.ForeignKey(User, null=True, on_delete=(models.CASCADE))
    source_display_name = models.CharField(max_length=150, null=True)
    recipient = models.ForeignKey(User,
      related_name='notifications', null=True, on_delete=(models.CASCADE))
    action = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    obj = models.IntegerField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    short_description = models.CharField(max_length=100)
    channels = ListField(max_length=200)
    extra_data = JSONField(default={})
    is_read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    objects = NotificationQuerySet.as_manager()

    def __str__(self):
        if self.source:
            res = '{}: {} {} {} => {}'.format(self.category, self.source, self.action, self.short_description, self.recipient)
        else:
            res = self.short_description
        return res

    def read(self):
        """Mark notification as read."""
        self.is_read = True
        self.save()

    def to_json(self):
        """
        Return JSON representation that can easily be serialized."""
        return {'source':getattr(self.source, 'id', ''), 
         'source_display_name':self.source_display_name, 
         'recipient':getattr(self.recipient, 'id', ''), 
         'category':self.category, 
         'action':self.action,  'obj':self.obj,  'short_description':self.short_description, 
         'url':self.url,  'channels':self.channels, 
         'extra_data':self.extra_data,  'is_read':self.is_read}