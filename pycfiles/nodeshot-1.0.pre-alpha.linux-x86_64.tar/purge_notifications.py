# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/community/notifications/management/commands/purge_notifications.py
# Compiled at: 2014-09-02 09:30:03
from django.core.management.base import BaseCommand
from nodeshot.community.notifications.models import Notification
from nodeshot.core.base.utils import ago
from ...settings import settings, DELETE_OLD

class Command(BaseCommand):
    help = 'Delete notifications older than DELETE_OLD'

    def retrieve_old_notifications(self):
        """
        Retrieve notifications older than X days, where X is specified in settings
        """
        date = ago(days=DELETE_OLD)
        return Notification.objects.filter(added__lte=date)

    def output(self, message):
        self.stdout.write('%s\n\r' % message)

    def handle(self, *args, **options):
        """ Purge notifications """
        notifications = self.retrieve_old_notifications()
        count = len(notifications)
        if count > 0:
            self.output('found %d notifications to purge...' % count)
            notifications.delete()
            self.output('%d notifications deleted successfully.' % count)
        else:
            self.output('there are no old notifications to purge')