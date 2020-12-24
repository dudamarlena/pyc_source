# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dependencyinjection\internal\servicesmap.py
# Compiled at: 2018-01-23 08:16:13
# Size of source mod 2**32: 960 bytes
import typing
from .descriptors import Descriptor

class ServicesMap:

    def __init__(self, services: typing.List[Descriptor]):
        self._type_map = {}
        for service in services:
            ls = self._type_map.get(service.service_type)
            if ls is None:
                ls = []
                self._type_map[service.service_type] = ls
            ls.append(service)

    def get(self, service_type: type) -> Descriptor:
        """return None is not found."""
        ls = self._type_map.get(service_type)
        if ls:
            return ls[(-1)]

    def getall(self, service_type: type) -> typing.List[Descriptor]:
        """return None is not found."""
        return self._type_map.get(service_type)