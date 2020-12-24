# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kyzima-spb/www/django-projects/mosginfo/adminlte_full/notifications.py
# Compiled at: 2016-04-14 16:07:44
# Size of source mod 2**32: 1049 bytes
import django.dispatch

class NotificationItem(object):
    TYPE_ERROR = 'red'
    TYPE_INFO = 'aqua'
    TYPE_SUCCESS = 'green'
    TYPE_WARNING = 'yellow'

    def __init__(self, message=None, icon=None, tp=None, uid=None):
        self._NotificationItem__uid = uid
        self.icon = icon
        self.message = message
        self.type = tp or self.TYPE_INFO

    @property
    def uid(self):
        return self._NotificationItem__uid


class NotificationList(object):
    show_signal = django.dispatch.Signal()

    def __init__(self):
        self._NotificationList__notifications = []

    def add_notification(self, notification):
        if isinstance(notification, NotificationItem):
            self._NotificationList__notifications.append(notification)

    @property
    def notifications(self):
        return self._NotificationList__notifications

    @notifications.setter
    def notifications(self, notifications):
        for note in notifications:
            self.add_notification(note)

    @property
    def total(self):
        return len(self.notifications)