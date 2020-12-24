# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wisestork/utils.py
# Compiled at: 2019-06-13 09:37:57
# Size of source mod 2**32: 3988 bytes
"""
wisestork.utils
~~~~~~~~~~~~~

:copyright: (c) 2016-2019 Sander Bollen
:license: GPL-3.0
"""
from collections import namedtuple
Bin = namedtuple('Bin', ['start', 'end'])

def utf8(value):
    if isinstance(value, bytes):
        return value
    else:
        if not isinstance(value, str):
            value = str(value)
        return bytes(value, 'utf-8')


def as_str(value):
    if isinstance(value, bytes):
        return value.decode()
    else:
        return value


class BedLine(namedtuple('BedLine', ['chromosome', 'start', 'end', 'value'])):
    __slots__ = ()

    def __str__(self):
        return '{0}\t{1}\t{2}\t{3}'.format(as_str(self.chromosome), self.start, self.end, as_str(self.value))

    def __bytes__(self):
        return (b'\t').join(map(utf8, [getattr(self, x) for x in self._fields]))

    def __eq__(self, other):
        return self.chromosome == other.chromosome and self.start == other.start and self.end == other.end

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def fromline(cls, line, sep=b'\t'):
        contents = utf8(line).split(sep)
        if len(contents) == 3:
            return cls(*map(attempt_numeric, contents), **{'value': 'NA'})
        else:
            return cls(*map(attempt_numeric, contents))


def attempt_numeric(value):
    """
    Attempt to make an numeric from a string
    first try to make an integer
    When that is not possible, make a float.
    When that too fails, return the string
    :param value: the input string
    :return: the possibly-converted item
    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def get_bins(chromosome_length, binsize):
    """
    Get list of 2-tuples of start and end positions of bins for a given
    chromosome
    :param chromosome_length: integer
    :param binsize: integer
    :return: list of 2-tuples of (start, end). Start = 0-based
    """
    starts = list(range(0, chromosome_length, binsize))
    ends = []
    for s in starts:
        if s + binsize < chromosome_length:
            ends.append(s + binsize)
        else:
            ends.append(chromosome_length)

    return [Bin(s, e) for s, e in zip(starts, ends)]


class BedReader(object):
    __doc__ = "\n    Iterator for reading bed files\n    Returns instances of BedLine\n\n    If no value is found in the 4th column, val = 'NA'\n    "

    def __init__(self, filename):
        self.filename = filename
        self._BedReader__handle = open(self.filename, 'rb')

    def __iter__(self):
        return self

    def __next__(self):
        try:
            line = self._BedReader__handle.readline()
        except StopIteration:
            self._BedReader__handle.close()
            raise StopIteration

        contents = line.strip().split(b'\t')
        if len(contents) == 3:
            return BedLine(*map(attempt_numeric, contents), **{'value': 'NA'})
        if len(contents) == 4:
            return BedLine(*map(attempt_numeric, contents))
        self._BedReader__handle.close()
        raise StopIteration

    def next(self):
        return self.__next__()