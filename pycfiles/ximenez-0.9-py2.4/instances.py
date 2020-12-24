# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/ximenez/collectors/zope/instances.py
# Compiled at: 2007-11-10 08:06:38
"""Define ``ZopeInstances``, which can collect Zope instances.

$Id: instances.py 8 2007-11-10 13:06:44Z damien.baty $
"""
from ximenez.collectors.collector import Collector
from ximenez.shared.zope import ZopeInstance

def getInstance():
    """Return an instance of ``ZopeInstances``."""
    return ZopeInstances()


class ZopeInstances(Collector):
    """A collector which returns instances of Zope servers.

    It asks for the location of the host (which can be its IP or its
    name) and the port which it listens HTTP connections on.

    Returns a tuple of ``ZopeInstance`` instances.
    """
    __module__ = __name__
    _input_info = ({'name': 'host', 'prompt': 'Host: ', 'required': True}, {'name': 'port', 'prompt': 'HTTP port: ', 'required': True})
    _multiple_input = True

    def collect(self):
        """Return a tuple of ``ZopeInstance`` instances."""
        return [ ZopeInstance(item['host'], item['port'])
         for item in self._input ]