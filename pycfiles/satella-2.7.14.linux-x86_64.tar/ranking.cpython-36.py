# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/structures/ranking.py
# Compiled at: 2020-04-25 10:46:39
# Size of source mod 2**32: 2790 bytes
import collections, typing as tp
from .sorted_list import SortedList
__all__ = [
 'Ranking']
T = tp.TypeVar('T')

class Ranking(tp.Generic[T]):
    __doc__ = "\n    A set of objects with them being ranked by their single property with the assumption that this\n    property changes only when we want to.\n\n    Positions are counted from 0, where 0 has the least key value.\n\n    Essentially, this is a SortedList with the option to query at which position can be given\n    element found.\n\n    Example usage:\n\n    >>> Entry = collections.namedtuple('Entry', ('key', ))\n    >>> e1 = Entry(2)\n    >>> e2 = Entry(3)\n    >>> e3 = Entry(5)\n    >>> ranking = Ranking([e1, e2, e3], lambda e: e.key)\n    >>> assert ranking[0] == e1     # Get the first element\n    >>> assert ranking[-1] == e3    # Get the last element\n    >>> assert ranking.get_position_of(e1) == 0\n    "
    __slots__ = ('items', 'key', 'ranking', 'element_to_position')

    def __init__(self, items: tp.List[T], key: tp.Callable[([T], int)]):
        self.items = items
        self.key = key
        self.ranking = SortedList(items, key=key)
        self.element_to_position = {}
        for position, item in enumerate(self.ranking):
            self.element_to_position[id(item)] = position

    def calculate_ranking_for(self, item: T) -> int:
        return self.element_to_position[id(item)]

    def add(self, item: T) -> None:
        """
        Add a single element to the ranking and recalculate it
        """
        index = self.ranking.add(item)
        for position, item in enumerate((self.ranking[index:]), start=index):
            self.element_to_position[id(item)] = position

    def remove(self, item: T) -> None:
        """
        Remove a single element from the ranking and recalculate it
        """
        index = self.ranking.index(item)
        self.ranking.remove(item)
        for position, item in enumerate((self.ranking[index:]), start=index):
            self.element_to_position[id(item)] = position

    def get_position_of(self, item: T) -> int:
        """
        Return the position in the ranking of element item

        :param item: element to return the position for
        :return: position
        :raises ValueError: this element is not in the ranking
        """
        return self.ranking.index(item)

    def __getitem__(self, item: int) -> T:
        """
        Return n-th item in ranking.

        :param item: position in ranking. Can be negative, or even a slice
        """
        return self.ranking[item]

    def get_sorted(self) -> tp.Iterator[T]:
        """
        Return all the elements sorted from the least key value to the highest key value
        """
        yield from self.ranking
        if False:
            yield None