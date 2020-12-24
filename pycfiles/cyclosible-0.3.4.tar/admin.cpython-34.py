# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/DATA-LINUX/Cycloid/Cyclosible/cyclosible/playbook/admin.py
# Compiled at: 2015-10-28 10:50:15
# Size of source mod 2**32: 534 bytes
from django.contrib import admin
from .models import Playbook, PlaybookRunHistory
from guardian.admin import GuardedModelAdmin

@admin.register(Playbook)
class PlaybookAdmin(GuardedModelAdmin):
    queryset = Playbook.objects.all()
    list_display = ('name', 'group', 'only_tags', 'skip_tags')


@admin.register(PlaybookRunHistory)
class PlaybookRunHistoryAdmin(GuardedModelAdmin):
    queryset = PlaybookRunHistory.objects.all()
    list_display = ('playbook', 'date_launched', 'date_finished', 'status', 'task_id',
                    'launched_by')