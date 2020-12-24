# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gthomas/dev/management-server/managementserver/django_sql_dashboards/filters.py
# Compiled at: 2014-02-16 11:51:21
from django.contrib.auth.models import User
from models import Query, Dashboard, DbConfig
import django_filters

class QueryFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_type='icontains')
    db = django_filters.ModelChoiceFilter(queryset=DbConfig.objects.exclude(query=None), widget=django_filters.widgets.LinkWidget)
    creator = django_filters.ModelChoiceFilter(queryset=User.objects.exclude(query=None), widget=django_filters.widgets.LinkWidget)

    class Meta:
        model = Query
        fields = ['title', 'creator', 'db']


class DashboardFilter(django_filters.FilterSet):
    creator = django_filters.ModelChoiceFilter(queryset=User.objects.exclude(query=None), widget=django_filters.widgets.LinkWidget)

    class Meta:
        model = Dashboard
        fields = ['creator']