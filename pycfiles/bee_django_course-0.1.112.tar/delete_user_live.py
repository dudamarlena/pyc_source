# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/management/commands/delete_user_live.py
# Compiled at: 2019-10-15 04:30:47
import time, datetime
from django.core.management.base import BaseCommand
from bee_django_course.models import UserLive
from django.utils import timezone
from bee_django_course import cc

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('days', type=int, nargs='?', default=20)

    def handle(self, *args, **options):
        days = options['days']
        print ('days', days)
        return
        for e in UserLive.objects.filter(created_at__lt=timezone.now() - datetime.timedelta(days=days), status=1):
            if e.provider_name == 'cc':
                if e.record_video_id and e.record_status == '10':
                    cc.delete_video(e.record_video_id)
            elif e.provider_name == 'gensee':
                pass
            elif e.provider_name == 'tencent':
                pass
            e.status = 2
            e.save()
            time.sleep(1)