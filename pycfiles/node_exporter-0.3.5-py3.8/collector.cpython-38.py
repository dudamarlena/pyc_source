# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/node_exporter/collector/collector.py
# Compiled at: 2020-01-14 05:18:01
# Size of source mod 2**32: 409 bytes
from prometheus_client.core import REGISTRY

class Collector(object):
    name: str
    isRegister = False
    isRegister: bool

    def collect(self):
        pass

    def register(self):
        if not self.isRegister:
            REGISTRY.register(self)
            self.isRegister = True

    def unregister(self):
        if self.isRegister:
            REGISTRY.unregister(self)
            self.isRegister = False