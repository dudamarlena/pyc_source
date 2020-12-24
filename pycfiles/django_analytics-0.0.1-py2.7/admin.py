# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/analytics/admin.py
# Compiled at: 2011-05-24 10:06:33
from django.contrib import admin
from analytics import models

class MetricAdmin(admin.ModelAdmin):
    list_display = [
     'uid', 'title']


admin.site.register(models.Metric, MetricAdmin)

class StatisticAdmin(admin.ModelAdmin):
    list_display = [
     'metric', 'date_time', 'frequency', 'count', 'cumulative_count']
    list_filter = ['frequency', 'metric', 'date_time']


admin.site.register(models.Statistic, StatisticAdmin)