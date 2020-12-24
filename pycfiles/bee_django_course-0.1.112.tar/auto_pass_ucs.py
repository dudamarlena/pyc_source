# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/management/commands/auto_pass_ucs.py
# Compiled at: 2019-10-30 04:13:08
import time, datetime
from django.core.management.base import BaseCommand
from bee_django_course.models import UserCourseSection
from django.utils import timezone

class Command(BaseCommand):

    def handle(self, *args, **options):
        ucs_list = UserCourseSection.objects.filter(section__auto_pass=True, status=1, section__pass_cooldown__gt=0)
        i = 0
        for ucs in ucs_list:
            if ucs.pass_check():
                ucs.get_pass()
                i += 1

        print '[' + timezone.localtime().strftime('%Y-%m-%d %H:%M:%S') + '] auto_pass_count: ' + i.__str__() + '/' + ucs_list.count().__str__()