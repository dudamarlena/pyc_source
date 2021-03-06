# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyquchk/lazylist.py
# Compiled at: 2013-09-21 05:07:46
from itertools import count

class LazyList(object):
    """A Sequence whose values are computed lazily by an iterator.

    .. ipython::

        >>> it = count()

        >>> ll = LazyList(it)

        >>> list(ll[:10])
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        >>> list(ll[:10])
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        >>> list(ll[:10])
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        >>> ll[123]
        123

        >>> list(ll[1:10:2])
        [1, 3, 5, 7, 9]
    """

    def __init__(self, iterable):
        self._exhausted = False
        self._iterator = iter(iterable)
        self._data = []

    def __len__(self):
        """Get the length of a LazyList's computed data."""
        return len(self._data)

    def __getitem__(self, i):
        """Get an item from a LazyList.
        i should be a positive integer or a slice object."""
        if isinstance(i, int):
            if i >= len(self):
                self.exhaust(i)
            elif i < 0:
                raise ValueError('cannot index LazyList with negative number')
            return self._data[i]
        else:
            if isinstance(i, slice):
                start, stop, step = i.start, i.stop, i.step
                if any(x is not None and x < 0 for x in (start, stop, step)):
                    raise ValueError('cannot index or step through a LazyList witha negative number')
                if start is None:
                    start = 0
                if step is None:
                    step = 1

                def LazyListIterator():
                    count = start
                    while stop is None or count < stop:
                        try:
                            yield self[count]
                        except IndexError:
                            break

                        count += step

                    return

                return LazyListIterator()
            raise TypeError('i must be an integer or slice')
            return

    def __iter__(self):
        """Return an iterator over each value in the sequence,
        whether it has been computed yet or not."""
        return self[:]

    def computed(self):
        """Return an iterator over the values in a LazyList that have
        already been computed."""
        return self[:len(self)]

    def exhaust(self, index=None):
        """Exhaust the iterator generating this LazyList's values.
        if index is None, this will exhaust the iterator completely.
        Otherwise, it will iterate over the iterator until either the list
        has a value for index or the iterator is exhausted.
        """
        if self._exhausted:
            return
        else:
            if index is None:
                ind_range = count(len(self))
            else:
                ind_range = range(len(self), index + 1)
            for ind in ind_range:
                try:
                    self._data.append(next(self._iterator))
                except StopIteration:
                    self._exhausted = True
                    break

            return