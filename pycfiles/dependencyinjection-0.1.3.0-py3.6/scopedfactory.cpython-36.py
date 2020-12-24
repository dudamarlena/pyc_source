# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dependencyinjection\internal\scopedfactory.py
# Compiled at: 2017-12-17 03:21:47
# Size of source mod 2**32: 489 bytes
from .common import IScopedFactory, IServiceProvider
from .provider import ServiceProvider

class ScopedFactory(IScopedFactory):

    def __init__(self, parent: IServiceProvider):
        self._service_provider = ServiceProvider(parent_provider=parent)

    @property
    def service_provider(self):
        return self._service_provider