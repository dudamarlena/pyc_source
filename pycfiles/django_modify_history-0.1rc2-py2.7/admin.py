# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/modify_history/admin.py
# Compiled at: 2011-06-10 23:28:22
from django.contrib import admin
from models import Timeline

class TimelineAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('label', 'url', 'action', 'user', 'created_at')
    list_filter = ('action', 'created_at', 'user')


admin.site.register(Timeline, TimelineAdmin)