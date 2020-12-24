# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/6z/y737zg156f53v6d096dlmv500000gn/T/pip-build-YeCYrE/user-behavior/user_behavior/filters.py
# Compiled at: 2016-11-17 22:38:22
import django_filters
from django_filters.filters import MethodFilter
from django.contrib.auth.models import User
from .models.api_info import ApiInfo
from .models.user_behavior import UserBehavior

class ApiInfoFilter(django_filters.FilterSet):
    user = MethodFilter(action='user_filter')
    status_code = MethodFilter(action='status_code_filter')

    class Meta:
        model = ApiInfo
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


class UserBehaviorFilter(django_filters.FilterSet):
    model = MethodFilter(action='model_filter')
    api_info = MethodFilter(action='api_info_filter')

    class Meta:
        model = UserBehavior
        fields = ('model', 'api_info')

    @classmethod
    def model_filter(cls, queryset, name):
        id_list = []
        for qs in queryset:
            if qs.content_type.model == name:
                id_list.append(qs.id)

        return queryset.filter(id__in=id_list)

    @classmethod
    def api_info_filter(cls, queryset, api_info):
        return queryset.filter(api_info__id=api_info)