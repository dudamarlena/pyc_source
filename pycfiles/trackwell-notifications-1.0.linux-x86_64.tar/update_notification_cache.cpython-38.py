# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/notifications/management/commands/update_notification_cache.py
# Compiled at: 2020-02-28 16:23:12
# Size of source mod 2**32: 530 bytes
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from accounts.models import UserNotification

class Command(BaseCommand):
    help = 'Updates cache entries for notifications'

    def handle(self, *args, **options):
        print('update_unseen_notification_cache')
        unseen = UserNotification.objects.all()
        for un in unseen:
            un.update_unseen_cache()
        else:
            print('Cache entries for {} notifications updated'.format(unseen.count()))