# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_zabbix/managers.py
# Compiled at: 2016-09-21 16:06:28
from nodeconductor.core.managers import GenericKeyMixin
from nodeconductor.structure.managers import StructureManager
from nodeconductor.structure.models import Resource, ResourceMixin

def filter_active(qs):
    INVALID_STATES = (
     Resource.States.PROVISIONING_SCHEDULED,
     Resource.States.PROVISIONING,
     Resource.States.DELETING,
     Resource.States.ERRED)
    return qs.exclude(backend_id='', state__in=INVALID_STATES)


class HostManager(GenericKeyMixin, StructureManager):
    """ Allows to filter and get hosts by generic key """

    def get_available_models(self):
        """ Return list of models that are acceptable """
        return ResourceMixin.get_all_models()