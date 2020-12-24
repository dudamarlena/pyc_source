# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/btrdb/point.py
# Compiled at: 2019-11-27 15:09:10
# Size of source mod 2**32: 6377 bytes
"""
Module for Point classes
"""
from btrdb.grpcinterface import btrdb_pb2

class RawPoint(object):
    __doc__ = '\n    A point of data representing a single position within a time series. Each\n    point contains a read-only time and value attribute.\n\n    Parameters\n    ----------\n    time : int\n        The time portion of a single value in the time series in nanoseconds\n        since the Unix epoch.\n    value : float\n        The value of a time series at a single point in time.\n\n    '
    __slots__ = [
     '_time', '_value']

    def __init__(self, time, value):
        self._time = time
        self._value = value

    @property
    def time(self):
        """
        The time portion of a data point in nanoseconds since the Unix epoch.
        """
        return self._time

    @property
    def value(self):
        """
        The value portion of a data point as a float object.
        """
        return self._value

    @classmethod
    def from_proto(cls, proto):
        return cls(proto.time, proto.value)

    @classmethod
    def from_proto_list(cls, proto_list):
        return [cls.from_proto(proto) for proto in proto_list]

    def __getitem__(self, index):
        if index == 0:
            return self.time
        if index == 1:
            return self.value
        raise IndexError('RawPoint index out of range')

    @staticmethod
    def to_proto(point):
        return btrdb_pb2.RawPoint(time=(point[0]), value=(point[1]))

    @staticmethod
    def to_proto_list(points):
        return [RawPoint.to_proto(p) for p in points]

    def __repr__(self):
        return 'RawPoint({0}, {1})'.format(repr(self.time), repr(self.value))

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return hasattr(other, 'time') and hasattr(other, 'value') or False
        return self.time == other.time and self.value == other.value


class StatPoint(object):
    __doc__ = '\n    An aggregated data point representing a summary or rollup of one or more\n    points of data within a single time series.\n\n    This aggregation point provides for the min, mean, max, count, and standard\n    deviation of all data values it spans.  It is returned by windowing queries\n    such as `windows` or `aligned_windows`.\n\n    Parameters\n    ----------\n    time : int\n        The time in which the aggregated values represent in nanoseconds since\n        the Unix epoch.\n    min : float\n        The minimum value in a time series within a specified range of time.\n    mean : float\n        The mean value in a time series within a specified range of time.\n    max : float\n        The maximum value in a time series within a specified range of time.\n    count : float\n        The number of values in a time series within a specified range of time.\n    stddev : float\n        The standard deviation of values in a time series within a specified\n        range of time.\n\n\n    Notes\n    -----\n    This object may also be treated as a tuple by referencing the values\n    according to position.\n\n    .. code-block:: python\n\n        // returns time\n        val = point[0]\n\n        // returns standard deviation\n        val = point[5]\n\n\n    '
    __slots__ = [
     '_time', '_min', '_mean', '_max', '_count', '_stddev']

    def __init__(self, time, minv, meanv, maxv, count, stddev):
        self._time = time
        self._min = minv
        self._mean = meanv
        self._max = maxv
        self._count = count
        self._stddev = stddev

    @classmethod
    def from_proto(cls, proto):
        return cls(proto.time, proto.min, proto.mean, proto.max, proto.count, proto.stddev)

    @classmethod
    def from_proto_list(cls, proto_list):
        return [cls.from_proto(proto) for proto in proto_list]

    @property
    def time(self):
        """
        The mean value of the time series point within a range of time
        """
        return self._time

    @property
    def min(self):
        """
        The minimum value of the time series within a range of time
        """
        return self._min

    @property
    def mean(self):
        """
        The mean value of the time series within a range of time
        """
        return self._mean

    @property
    def max(self):
        """
        The maximum value of the time series within a range of time
        """
        return self._max

    @property
    def count(self):
        """
        The number of values within the time series for a range of time
        """
        return self._count

    @property
    def stddev(self):
        """
        The standard deviation of the values of a time series within a range of time
        """
        return self._stddev

    def __getitem__(self, index):
        if index == 0:
            return self.time
        if index == 1:
            return self.min
        if index == 2:
            return self.mean
        if index == 3:
            return self.max
        if index == 4:
            return self.count
        if index == 5:
            return self.stddev
        raise IndexError('RawPoint index out of range')

    def __repr__(self):
        return 'StatPoint({}, {}, {}, {}, {}, {})'.format(self.time, self.min, self.mean, self.max, self.count, self.stddev)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        for attr in ('time', 'min', 'mean', 'max', 'count', 'stddev'):
            if not hasattr(other, attr):
                return False
            return self.time == other.time and self.min == other.min and self.mean == other.mean and self.max == other.max and self.count == other.count and self.stddev == other.stddev