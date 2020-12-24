# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/management/commands/close_finished_projects.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 558 bytes
import sys
from django.core.management.base import BaseCommand
from django.utils import timezone
from ovp_projects.models import Project

class Command(BaseCommand):
    help = 'Close projects which have a Job and end_date has already passed'

    def handle(self, *args, **options):
        projects = Project.objects.filter(closed=False, job__end_date__lt=timezone.now())
        print('Closing {} finished projects'.format(projects.count()))
        projects.update(closed=True)