# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sw_logger/filters.py
# Compiled at: 2019-01-10 10:18:30
import django_filters
from . import models

class Log(django_filters.FilterSet):
    datetime_from = django_filters.DateTimeFilter('created', lookup_expr='gte')
    datetime_to = django_filters.DateTimeFilter('created', lookup_expr='lte')
    message = django_filters.CharFilter('message', lookup_expr='icontains')
    action = django_filters.MultipleChoiceFilter('action', choices=models.Log.ACTION_CHOICES)
    level = django_filters.MultipleChoiceFilter('level', choices=models.Log.LOG_LEVEL_CHOICES)

    class Meta:
        model = models.Log
        fields = ['datetime_from', 'datetime_to', 'action', 'level', 'object_name', 'message', 'username']