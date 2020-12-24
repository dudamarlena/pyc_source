# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dependencyinjection\internal\service_resolver.py
# Compiled at: 2017-12-18 00:42:41
# Size of source mod 2**32: 1076 bytes
from .checker import CycleChecker

class IServiceResolver:

    def resolve(self, service_provider):
        raise NotImplementedError


class ServiceResolver(IServiceResolver):

    def __init__(self, service_type: type):
        assert service_type is not None
        self._service_type = service_type

    def resolve(self, service_provider):
        return service_provider._resolve(self._service_type, CycleChecker(), False)


class ListedServiceResolver(IServiceResolver):

    def __init__(self, service_type: type):
        assert service_type is not None
        self._service_type = service_type

    def resolve(self, service_provider):
        descriptors = service_provider._service_map.getall(self._service_type)
        ret = []
        if descriptors:
            for d in descriptors:
                ret.append(service_provider._resolve_by_descriptor(d, CycleChecker()))

        return ret