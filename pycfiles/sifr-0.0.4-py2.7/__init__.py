# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/sifr/__init__.py
# Compiled at: 2015-06-10 09:00:02
"""
"""
import time
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

class RPCClient(object):

    def __init__(self, host, port, resolutions=None):
        import msgpackrpc
        self.client = msgpackrpc.Client(msgpackrpc.Address(host, port), unpack_encoding='utf-8')
        self.resolutions = resolutions or ['year', 'month',
         'day', 'hour', 'minute']

    def incr(self, key, amount=1, resolutions=None):
        self.client.call('incr', key, resolutions or self.resolutions, amount)

    def incr_unique(self, key, identity, resolutions=None):
        self.client.call('incr_unique', key, resolutions or self.resolutions, identity)

    def track(self, key, identity, resolutions=None):
        self.client.call('track', key, resolutions or self.resolutions, identity)

    def count(self, key, at, resolution):
        return self.client.call('count', key, time.mktime(at.timetuple()), resolution)

    def cardinality(self, key, at, resolution):
        return self.client.call('cardinality', key, time.mktime(at.timetuple()), resolution)

    def uniques(self, key, at, resolution):
        return set(self.client.call('uniques', key, time.mktime(at.timetuple()), resolution))