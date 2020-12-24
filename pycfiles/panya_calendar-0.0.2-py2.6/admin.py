# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cal/admin.py
# Compiled at: 2011-03-28 05:04:09
from django.contrib import admin
from cal.models import Calendar, Entry
from panya.admin import ModelBaseAdmin

class EntryAdmin(admin.ModelAdmin):
    list_display = ('content', 'start', 'end', 'repeat', 'repeat_until')
    list_filter = ('repeat', )
    search_fields = ('content__title', 'content__description')


admin.site.register(Calendar, ModelBaseAdmin)
admin.site.register(Entry, EntryAdmin)