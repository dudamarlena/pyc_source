# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/chart/management/commands/chartupdate.py
# Compiled at: 2010-08-04 03:51:07
from django.core.management.base import BaseCommand
from chart.models import Chart

class Command(BaseCommand):

    def handle(self, *app_labels, **options):
        object_list = Chart.objects.all()
        for obj in object_list:
            for entry in obj.chartentries.all():
                if entry.remove:
                    entry.delete()
                else:
                    entry.previous_position = entry.current_position
                    entry.current_position = entry.next_position
                    entry.next_position = 0
                    entry.save()