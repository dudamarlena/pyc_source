# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/continuum.py
# Compiled at: 2010-11-14 19:22:11
from bisect import bisect_right
try:
    from hashlib import md5
except ImportError:
    from md5 import new as md5

import math, struct
DEFAULT_TOTAL_DOTS = 1000

class Server(object):
    """A server definition in the continuum."""
    __slots__ = ('hostname', 'port', 'capacity')

    def __init__(self, hostname, port, capacity):
        super(Server, self).__init__()
        self.hostname = hostname
        self.port = port
        self.capacity = capacity

    def __cmp__(self, other):
        assert isinstance(other, type(self))
        return cmp((self.hostname, self.port), (
         other.hostname, other.port))

    def __repr__(self):
        return '<%s "%s:%d", capacity=%d>' % (type(self).__name__,
         self.hostname, self.port, self.capacity)


class ContinuumEntry(object):
    """A server entry on the continuum."""
    __slots__ = ('position', 'server')

    def __init__(self, position, server):
        super(ContinuumEntry, self).__init__()
        self.position = position
        self.server = server

    def __cmp__(self, other):
        if isinstance(other, type(self)):
            other = other.position
        return cmp(self.position, other)

    def __repr__(self):
        return '<%s %d=%r>' % (type(self).__name__,
         self.position, self.server)


class Continuum(object):
    """The continuum that resolves a key to a server."""

    def __init__(self, totaldots=DEFAULT_TOTAL_DOTS, autogenerate=True):
        """Initialize new empty continuum."""
        super(Continuum, self).__init__()
        self.servers = []
        self.continuum = []
        self.totaldots = totaldots
        self.autogenerate = autogenerate

    def add_server(self, hostname, port, capacity=1):
        """Add a server definition with the given capacity."""
        server = Server(hostname, port, capacity)
        if server in self.servers:
            raise TypeError('server already added')
        self.servers.append(server)
        if self.autogenerate:
            self.generate()
        return server

    def remove_server(self, server):
        """Remove a server definition from the continuum."""
        self.servers.remove(server)
        if self.autogenerate:
            self.generate()

    def __len__(self):
        return len(self.servers)

    def _hash(self, key):
        """Return 4 hash values for the given key."""
        digest = md5(key).digest()
        return struct.unpack('<IIII', digest)

    def generate(self):
        """Generate the continuum from the list of servers."""
        capacity = float(sum([ x.capacity for x in self.servers ]))
        continuum = []
        for server in self.servers:
            dots = int(self.totaldots * (server.capacity / capacity))
            (d, m) = divmod(dots, 4)
            for x in xrange(d):
                positions = self._hash('%s-%d-%d' % (
                 server.hostname, server.port, x))
                for position in positions:
                    entry = ContinuumEntry(position, server)
                    continuum.append(entry)

            if m:
                positions = self._hash('%s-%d-%d' % (
                 server.hostname, server.port, d))
                for position in xrange(m):
                    entry = ContinuumEntry(position, server)
                    continuum.append(entry)

        continuum.sort()
        self.continuum = continuum

    def resolve(self, key):
        """Return the server for the given key."""
        if not self.continuum:
            raise IndexError('empty continuum')
        position = self._hash(key)[0]
        entry = bisect_right(self.continuum, position)
        try:
            return self.continuum[entry].server
        except IndexError:
            return self.continuum[0].server