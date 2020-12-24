# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/chart/admin.py
# Compiled at: 2010-08-04 03:51:07
from django.contrib import admin
from panya.admin import ModelBaseAdmin
from chart.models import Chart, ChartEntry, ChartPreferences

class ChartEntryAdmin(admin.ModelAdmin):
    list_display = ('chart', 'track', 'current_position', 'remove')
    list_filter = ('chart', 'created')
    search_fields = ('created', )


admin.site.register(Chart, ModelBaseAdmin)
admin.site.register(ChartEntry, ChartEntryAdmin)
admin.site.register(ChartPreferences)