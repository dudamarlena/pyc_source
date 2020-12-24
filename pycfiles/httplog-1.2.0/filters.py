# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\users\ma_k\appdata\local\temp\pip-build-s8wja0\httplog\httplog\filters.py
# Compiled at: 2016-11-28 21:21:16
import django_filters
from django_filters.filters import MethodFilter
from .models.httplog import HttpLog

class HttpLogFilter(django_filters.FilterSet):
    user = MethodFilter(action='user_filter')
    status_code = MethodFilter(action='status_code_filter')

    class Meta:
        model = HttpLog
        fields = ('user', 'status_code')

    @classmethod
    def user_filter(cls, queryset, username):
        return queryset.filter(user__username__contains=username)

    @classmethod
    def status_code_filter(cls, queryset, status_code):
        id_list = []
        for qs in queryset:
            if qs.response.has_key('status_code'):
                if qs.response['status_code'] == int(status_code):
                    id_list.append(qs.id)

        return queryset.filter(id__in=id_list)