# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/kdsearch/statistics.py
# Compiled at: 2017-03-03 07:36:48
# Size of source mod 2**32: 1651 bytes
import numpy

class Statistics:
    __doc__ = 'Represents a set of floats, allowing to retrieve its mean, without storing\n    all the individual floats\n    '

    def __init__(self, sum: float=0,
                 length: int=0):
        """
        >>> Statistics()
        Statistics(sum=0, length=0)
        >>> Statistics(sum=3, length=5)
        Statistics(sum=3, length=5)
        """
        self.sum = sum
        self.length = length

    def merge(self, other: 'Statistics'):
        """Merge another Statistics objects into this one

        >>> stats = Statistics(sum=1, length=1)
        >>> stats.merge(Statistics(sum=1, length=2))
        >>> stats
        Statistics(sum=2, length=3)
        """
        self.sum += other.sum
        self.length += other.length

    def mean(self) -> float:
        """Return the mean of the elements represented or 0 if there are no elements.

        >>> Statistics(sum=1, length=2).mean()
        0.5
        >>> Statistics(sum=0, length=0).mean()
        0
        """
        if self.length:
            return self.sum / self.length
        return 0

    def __len__(self):
        return self.length

    def __repr__(self):
        return 'Statistics(sum=%g, length=%d)' % (self.sum, self.length)

    @staticmethod
    def from_array(elems) -> 'Statistics':
        """Compute the statistics of an array of numbers.

        >>> Statistics.from_array([1,2,3])
        Statistics(sum=6, length=3)
        >>> Statistics.from_array([])
        Statistics(sum=0, length=0)
        """
        return Statistics(numpy.sum(elems), numpy.size(elems))


if __name__ == '__main__':
    import doctest
    doctest.testmod()