# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/management/commands/handlingobjectsupdates.py
# Compiled at: 2018-11-10 03:15:27
from __future__ import unicode_literals
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from django.core.management import call_command
User = get_user_model()

class Command(BaseCommand):
    help = b'handle update'

    def handle(self, *args, **options):
        start_time = now()
        call_command(b'courseindexing')
        call_command(b'reviewssummary')
        call_command(b'progresssummary')
        call_command(b'notifiesme')
        call_command(b'sendnotifications')
        finished_time = now()
        print b'handle objects update %s - time long: %ss.' % (now(), relativedelta(finished_time, start_time).seconds)