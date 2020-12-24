# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/insality/code/django/feed_test/newsletter/management/commands/mail_check.py
# Compiled at: 2014-04-19 00:24:34
from django.core.management.base import BaseCommand, CommandError
from newsletter.models import Job, MAIL_STATE_READY

class Command(BaseCommand):
    help = 'Проверяет все работы со состоянием "Ждет отправки", и если дата отправления наступила - отправляет их'

    def handle(self, *args, **options):
        print 'Проверка писем, готовых к отправке...'
        Job.check_schedule()