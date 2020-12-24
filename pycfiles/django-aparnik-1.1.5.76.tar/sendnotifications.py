# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/notifications/management/commands/sendnotifications.py
# Compiled at: 2018-11-10 03:15:27
from __future__ import unicode_literals
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from fcm_django.models import FCMDevice
from aparnik.contrib.notifications.models import Notification
from aparnik.contrib.basemodels.models import BaseModel
import datetime
User = get_user_model()

class Command(BaseCommand):
    help = b'send notification'

    def handle(self, *args, **options):
        start_time = now()
        if Notification.objects.update_needed().count() > 0:
            self.reindex()
        Notification.objects.update_needed().update(update_needed=False)
        finished_time = now()
        print b'send notifications %s - time long: %ss.' % (now(), relativedelta(finished_time, start_time).seconds)

    def reindex(self):
        for obj in Notification.objects.update_needed():
            try:
                devices = FCMDevice.objects.filter(user__in=obj.users.all())
                devices.send_message(title=obj.title, body=obj.description)
            except Exception as e:
                print e.message