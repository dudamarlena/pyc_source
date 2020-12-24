# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/btrdb/point.py
# Compiled at: 2019-11-27 15:09:10
# Size of source mod 2**32: 6377 bytes
__doc__ = '\nModule for Point classes\n'
from btrdb.grpcinterface import btrdb_pb2

class RawPoint(object):
    """RawPoint"""
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
        return hasattr(other, 'time') and hasattr(other, 'value') or 
        return self.time == other.time and self.value == other.value


class StatPoint(object):
    """StatPoint"""
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