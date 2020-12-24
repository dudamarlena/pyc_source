# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/ximenez/collectors/zope/readlines.py
# Compiled at: 2007-11-25 11:46:09
"""Define ``ZopeInstancesReadlines``, which can collect Zope instances
that are listed in a file.

$Id: readlines.py 30 2007-11-25 16:46:12Z damien.baty $
"""
from ximenez.shared.zope import ZopeInstance
from ximenez.collectors.misc.readlines import ReadLines as BaseReadlinesCollector

def getInstance():
    """Return an instance of ``ZopeInstancesReadlines``."""
    return ZopeInstancesReadlines()


class ZopeInstancesReadlines(BaseReadlinesCollector):
    """A collector which returns instances of Zope servers that are
    listed in a file.

    It asks for the pathname of the file whose lines should have the
    following format::

        <host>:<port>

    Returns a tuple of ``ZopeInstance`` instances.
    """
    __module__ = __name__

    def collect(self):
        """Return a tuple of ``ZopeInstance`` objects."""
        instances = []
        for line in BaseReadlinesCollector.collect(self):
            (host, port) = line.split(':')
            port = port.strip()
            instances.append(ZopeInstance(host, port))

        return instances