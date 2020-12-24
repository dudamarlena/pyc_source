# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flowproc/fluent.py
# Compiled at: 2019-07-08 19:44:31
# Size of source mod 2**32: 1057 bytes
import sys
from ipaddress import ip_address

class Fluent:

    def __init__(self, cache=None):
        self._cache = cache or []

    def _(self, name):
        return Fluent(self._cache + [name])

    def process(self, data):
        for func in self._cache:
            data = func(data)

    def __getattr__(self, name):
        obj = globals()[name]
        return self._(obj)

    def __del__(self):
        print('Deleting', self)


def to_ip(data):
    return ip_address(int(data))


def print_ip(data):
    print(data)
    return data


fluent = Fluent()
chain = fluent.to_ip.print_ip
chain.process(sys.argv[1] if len(sys.argv) > 1 else 0)