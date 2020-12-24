# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/plugins/base/notifier.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
__all__ = ('Notifier', )
from sentry import ratelimits

class Notifier(object):

    def notify(self, notification, **kwargs):
        """
        Send a notification.

        See :class:`sentry.plugins.Notification` for notification properties.

        >>> def notify(self, notification):
        >>>     self.logger.info('Received notification for event %r', notification.event)
        """
        pass

    def should_notify(self, group, event):
        if group.is_ignored():
            return False
        project = group.project
        rate_limited = ratelimits.is_limited(project=project, key=self.get_conf_key(), limit=10)
        if rate_limited:
            self.logger.info('notification.rate_limited', extra={'project_id': project.id})
        return not rate_limited

    def notify_about_activity(self, activity):
        pass