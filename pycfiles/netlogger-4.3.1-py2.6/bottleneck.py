# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/bottleneck.py
# Compiled at: 2009-12-08 17:43:28
"""
Algorithms for determining the bottleneck in a disk-to-disk
file transfer.
"""
import operator

class Event:
    DISK_READ = 'disk.read'
    DISK_WRITE = 'disk.write'
    NET_READ = 'net.read'
    NET_WRITE = 'net.write'

    @staticmethod
    def get(name):
        for e in (Event.DISK_READ, Event.DISK_WRITE,
         Event.NET_READ, Event.NET_WRITE):
            if e in name:
                return e


class Value:

    def __init__(self, event, bytes_per_sec):
        self.event = event
        self.value = bytes_per_sec

    def __str__(self):
        return '%s=%lf' % (self.event, self.value)


class BottleneckAlgorithm:
    """
    Interface for bottleneck detection algorithms.
    """

    def sortedValues(self, values):
        """Return sorted copy of list of (object, value),
        sorted by the value
        """
        return sorted(values, key=operator.attrgetter('value'))

    def calculate(self, values):
        """Calculate bottleneck for the given values.
        The values are a list of instances of the Values class.
        Return a pair (Value, string) which identifies the bottleneck
        and a string explaining why.
        """
        pass

    def __str__(self):
        return 'bottleneck algorithm %s' % self.name


class Method1(BottleneckAlgorithm):

    def __init__(self, epsilon=0.15):
        """Initialize with the fraction of difference
        between two values that is considered significant
        """
        self._epsmult = 1 + epsilon

    def _different(self, x, y):
        if x > y:
            y, x = x, y
        return y > x * self._epsmult

    def calculate(self, values):
        E = Event
        v = self.sortedValues(values)
        slowest = self._different(v[0].value, v[1].value)
        if slowest and v[0].event in (E.DISK_READ, E.NET_READ, E.DISK_WRITE):
            bottleneck = (
             v[0], '')
        elif v[0].event == E.DISK_WRITE and v[1].event == E.NET_READ:
            bottleneck = (
             v[0], 'probably pushed back on net read')
        else:
            bottleneck = (None, '')
        return bottleneck