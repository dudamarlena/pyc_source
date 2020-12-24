# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dependencyinjection\internal\checker.py
# Compiled at: 2018-01-23 08:13:06
# Size of source mod 2**32: 828 bytes
from .errors import CycleDependencyError

class CycleChecker:

    def __init__(self):
        self._chain = []
        self._chain_set = set()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.remove_last()

    def add_or_raise(self, service_type: type):
        self._chain.append(service_type)
        if service_type in self._chain_set:
            msg = ' -> '.join([str(x.__name__) for x in self._chain])
            raise CycleDependencyError(msg)
        self._chain_set.add(service_type)
        return self

    def remove_last(self):
        self._chain_set.remove(self._chain.pop())