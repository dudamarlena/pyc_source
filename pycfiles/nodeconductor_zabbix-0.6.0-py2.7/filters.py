# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_zabbix/filters.py
# Compiled at: 2016-09-21 16:06:28
import django_filters
from nodeconductor.core import filters as core_filters
from nodeconductor.core.filters import UUIDFilter
from nodeconductor.structure import models as structure_models
from nodeconductor.structure.filters import ServicePropertySettingsFilter
from . import models

class HostScopeFilterBackend(core_filters.GenericKeyFilterBackend):

    def get_related_models(self):
        return structure_models.ResourceMixin.get_all_models()

    def get_field_name(self):
        return 'scope'


class TriggerFilter(ServicePropertySettingsFilter):
    template = core_filters.URLFilter(view_name='zabbix-template-detail', name='template__uuid', distinct=True)
    template_uuid = UUIDFilter(name='template__uuid')

    class Meta(ServicePropertySettingsFilter.Meta):
        model = models.Trigger
        fields = ServicePropertySettingsFilter.Meta.fields + ('template', 'template_uuid')


class UserFilter(ServicePropertySettingsFilter):
    surname = django_filters.CharFilter(lookup_type='icontains')
    alias = django_filters.CharFilter(lookup_type='icontains')

    class Meta(ServicePropertySettingsFilter.Meta):
        model = models.User
        fields = ServicePropertySettingsFilter.Meta.fields + ('alias', 'surname')