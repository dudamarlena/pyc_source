# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_looking_glass/filters.py
# Compiled at: 2016-07-18 08:21:15
# Size of source mod 2**32: 4901 bytes
"""
Admin settings for the dhcpkit looking glass
"""
from datetime import timedelta
from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from django.db.models.aggregates import Count
from django.db.models.expressions import F, Value
from django.db.models.functions import Concat
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import ugettext_lazy as _
from typing import Tuple, Iterable
from dhcpkit_looking_glass.models import Client

class ResponseFilter(SimpleListFilter):
    __doc__ = '\n    Filter on response statistics\n    '
    title = _('Response statistics')
    parameter_name = 'response_stat'

    def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin) -> Iterable[Tuple[(str, str)]]:
        """
        Which filters do we provide?

        :param request: The incoming request
        :param model_admin:
        :return: A list of lookups
        """
        return (
         (
          'slow', _('Slow responses (>1s)')),
         (
          'no', _('No response')))

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:
        """
        Adjust the queryset based on the selection

        :param request: The incoming request
        :param queryset: The original queryset
        :return: The modified queryset
        """
        val = self.value()
        if val == 'slow':
            return queryset.filter(response_ts__gt=F('request_ts') + timedelta(seconds=1))
        else:
            if val == 'no':
                return queryset.filter(response='')
            return queryset


class MultipleDUIDFilter(SimpleListFilter):
    __doc__ = '\n    Filter on multiple DUIDs per remote-id/interface-id\n    '
    title = _('Multiple DUIDs')
    parameter_name = 'multi_duid'

    def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin) -> Iterable[Tuple[(str, str)]]:
        """
        Which filters do we provide?

        :param request: The incoming request
        :param model_admin:
        :return: A list of lookups
        """
        return (
         (
          'per_interface_id', _('per Interface-ID')),
         (
          'per_remote_id', _('per Remote-ID')),
         (
          'per_combined', _('per combination of both')))

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:
        """
        Adjust the queryset based on the selection

        :param request: The incoming request
        :param queryset: The original queryset
        :return: The modified queryset
        """
        val = self.value()
        if val == 'per_interface_id':
            return queryset.filter(interface_id__in=Client.objects.values('interface_id').annotate(duid_count=Count('duid')).filter(duid_count__gt=1).values('interface_id'))
        else:
            if val == 'per_remote_id':
                return queryset.filter(remote_id__in=Client.objects.values('remote_id').annotate(duid_count=Count('duid')).filter(duid_count__gt=1).values('remote_id'))
            if val == 'per_combined':
                return queryset.annotate(concat_id=Concat('remote_id', Value('|'), 'interface_id')).filter(concat_id__in=Client.objects.values('interface_id', 'remote_id').annotate(duid_count=Count('duid')).filter(duid_count__gt=1).annotate(concat_id=Concat('remote_id', Value('|'), 'interface_id')).values('concat_id'))
            return queryset


class DuplicateDUIDFilter(SimpleListFilter):
    __doc__ = '\n    Filter on multiple DUIDs per remote-id/interface-id\n    '
    title = _('Duplicate DUIDs')
    parameter_name = 'duplicate_duid'

    def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin) -> Iterable[Tuple[(str, str)]]:
        """
        Which filters do we provide?

        :param request: The incoming request
        :param model_admin:
        :return: A list of lookups
        """
        return (
         (
          'yes', _('DUID on different ports')),)

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:
        """
        Adjust the queryset based on the selection

        :param request: The incoming request
        :param queryset: The original queryset
        :return: The modified queryset
        """
        val = self.value()
        if val == 'yes':
            return queryset.filter(duid__in=Client.objects.values('duid').annotate(port_count=Count('interface_id', 'remote_id')).filter(port_count__gt=1).values('duid'))
        else:
            return queryset