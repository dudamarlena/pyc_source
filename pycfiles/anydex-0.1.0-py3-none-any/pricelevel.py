# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/core/pricelevel.py
# Compiled at: 2019-05-25 07:31:00


class PriceLevel(object):
    """Class to represents a list of ticks at a specific price level"""

    def __init__(self, price):
        self._head_tick = None
        self._tail_tick = None
        self._length = 0
        self._depth = 0
        self._last = None
        self._price = price
        return

    @property
    def price(self):
        """
        :rtype: Price
        """
        return self._price

    @property
    def first_tick(self):
        """
        :rtype: TickEntry
        """
        return self._head_tick

    @property
    def length(self):
        """
        Return the length of the amount of ticks contained in the price level
        :rtype: int
        """
        return self._length

    @property
    def depth(self):
        """
        The depth is equal to the total amount of volume contained in this price level
        :rtype: int
        """
        return self._depth

    @depth.setter
    def depth(self, new_depth):
        """
        :param new_depth: The new depth
        :type new_depth: int
        """
        self._depth = new_depth

    def __len__(self):
        """
        Return the length of the amount of ticks contained in the price level
        """
        return self.length

    def __iter__(self):
        self._last = self._head_tick
        return self

    def __next__(self):
        """
        Return the next tick in the price level for the iterator
        """
        if self._last is None:
            raise StopIteration
        else:
            return_value = self._last
            self._last = self._last.next_tick
            return return_value
        return

    def next(self):
        return self.__next__()

    def append_tick(self, tick):
        """
        :type tick: TickEntry
        """
        if self._length == 0:
            tick.prev_tick = None
            tick.next_tick = None
            self._head_tick = tick
            self._tail_tick = tick
        else:
            tick.prev_tick = self._tail_tick
            tick.next_tick = None
            self._tail_tick.next_tick = tick
            self._tail_tick = tick
        self._length += 1
        self._depth += tick.assets.first.amount
        return

    def remove_tick(self, tick):
        """
        Remove a specific tick from the price level.

        :param tick: The tick to be removed
        :type tick: TickEntry
        """
        self._depth -= tick.assets.first.amount
        self._length -= 1
        if self._length == 0:
            return
        else:
            prev_tick = tick.prev_tick
            next_tick = tick.next_tick
            if prev_tick is not None and next_tick is not None:
                prev_tick.next_tick = next_tick
                next_tick.prev_tick = prev_tick
            elif next_tick is not None:
                next_tick.prev_tick = None
                self._head_tick = next_tick
            elif prev_tick is not None:
                prev_tick.next_tick = None
                self._tail_tick = prev_tick
            return

    def __str__(self):
        res_str = ''
        for tick in self:
            res_str += '%s\n' % str(tick)

        return res_str