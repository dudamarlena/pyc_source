# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/btrdb/utils/general.py
# Compiled at: 2019-06-17 14:48:35
# Size of source mod 2**32: 4855 bytes
"""
General utilities for btrdb bindings
"""

def unpack_stream_descriptor(desc):
    """
    Returns dicts for tags and annotations found in supplied stream
    """
    tags = {}
    for tag in desc.tags:
        tags[tag.key] = tag.val.value
    else:
        anns = {}
        for ann in desc.annotations:
            anns[ann.key] = ann.val.value
        else:
            return (
             tags, anns)


class pointwidth(object):
    __doc__ = '\n    A representation of a period of time described by the BTrDB tree (and used in\n    aligned_windows queries). The pointwidth allows users to traverse to different\n    levels of the BTrDB tree and to select StatPoints directly, vastly improving the\n    performance of queries. However, because the real duration of the pointwidth is\n    defined in powers of 2 (e.g. 2**pointwidth nanoseconds), the durations do not map\n    to human time periods (e.g. weeks or hours).\n\n    Parameters\n    ----------\n    p : int\n        cast an integer to the specified pointwidth\n    '

    @classmethod
    def from_timedelta(cls, delta):
        """
        Returns the closest pointwidth for the given timedelta without going over the
        specified duration. Because pointwidths are in powers of 2, be sure to check
        that the returned real duration is sufficient.
        """
        return cls.from_nanoseconds(delta.total_seconds() * 1000000000.0)

    @classmethod
    def from_nanoseconds(cls, nsec):
        """
        Returns the closest pointwidth for the given number of nanoseconds without going
        over the specified duration. Because pointwidths are in powers of 2, be sure to
        check that the returned real duration is sufficient.
        """
        for pos in range(62):
            nsec = nsec >> 1
            if nsec == 0:
                break
            return cls(pos)

    def __init__(self, p):
        self._pointwidth = int(p)

    @property
    def nanoseconds(self):
        return 2 ** self._pointwidth

    @property
    def microseconds(self):
        return self.nanoseconds / 1000.0

    @property
    def milliseconds(self):
        return self.nanoseconds / 1000000.0

    @property
    def seconds(self):
        return self.nanoseconds / 1000000000.0

    @property
    def minutes(self):
        return self.nanoseconds / 60000000000.0

    @property
    def hours(self):
        return self.nanoseconds / 3600000000000.0

    @property
    def days(self):
        return self.nanoseconds / 86400000000000.0

    @property
    def weeks(self):
        return self.nanoseconds / 604800000000000.0

    @property
    def months(self):
        return self.nanoseconds / 2628000000000000.0

    @property
    def years(self):
        return self.nanoseconds / 3.154e+16

    def decr(self):
        return pointwidth(self - 1)

    def incr(self):
        return pointwidth(self + 1)

    def __int__(self):
        return self._pointwidth

    def __eq__(self, other):
        return int(self) == int(other)

    def __lt__(self, other):
        return int(self) < int(other)

    def __le__(self, other):
        return int(self) <= int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __ge__(self, other):
        return int(self) >= int(other)

    def __add__(self, other):
        return pointwidth(int(self) + int(other))

    def __sub__(self, other):
        return pointwidth(int(self) - int(other))

    def __str__(self):
        """
        Returns the pointwidth to the closest unit
        """
        if self >= 55:
            return '{:0.2f} years'.format(self.years)
        if self >= 52:
            return '{:0.2f} months'.format(self.months)
        if self >= 50:
            return '{:0.2f} weeks'.format(self.weeks)
        if self >= 47:
            return '{:0.2f} days'.format(self.days)
        if self >= 42:
            return '{:0.2f} hours'.format(self.hours)
        if self >= 36:
            return '{:0.2f} minutes'.format(self.minutes)
        if self >= 30:
            return '{:0.2f} seconds'.format(self.seconds)
        if self >= 20:
            return '{:0.2f} milliseconds'.format(self.milliseconds)
        if self >= 10:
            return '{:0.2f} microseconds'.format(self.microseconds)
        return '{:0.0f} nanoseconds'.format(self.nanoseconds)

    def __repr__(self):
        return '<pointwidth {}>'.format(int(self))