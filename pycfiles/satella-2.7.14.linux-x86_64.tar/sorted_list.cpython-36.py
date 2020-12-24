# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/structures/sorted_list.py
# Compiled at: 2020-04-25 10:46:39
# Size of source mod 2**32: 4178 bytes
import collections, typing as tp
__all__ = [
 'SortedList', 'SliceableDeque']
T = tp.TypeVar('T')

class SortedList(tp.Generic[T]):
    __doc__ = "\n    An always-sorted sort of a set\n\n    It is assumed that keys of constituent elements don't change.\n\n    list[0] will have the smallest element, and list[-1] the biggest\n\n    :param items: items to construct the list with\n    :param key: a callable[T]->int that builds the key of the sort\n    "
    __slots__ = ('items', 'keys', 'key')

    def __init__(self, items: tp.Iterable[T]=(), key: tp.Callable[([T], int)]=lambda a: a):
        sort = sorted((key(item), item) for item in items)
        self.items = SliceableDeque(a[1] for a in sort)
        self.keys = collections.deque(a[0] for a in sort)
        self.key = key

    def __contains__(self, item: T) -> bool:
        return item in self.items

    def pop(self) -> T:
        """Return the highest element, removing it from the list"""
        self.keys.pop()
        return self.items.pop()

    def popleft(self) -> T:
        """Return the smallest element, removing it from the list"""
        self.keys.popleft()
        return self.items.popleft()

    def __iter__(self) -> tp.Iterator[T]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def index(self, other: T) -> int:
        """Return index at which given value has been placed"""
        return self.items.index(other)

    def extend(self, elements: tp.Iterable[T]):
        """Adds multiple elements to this list"""
        for elem in elements:
            self.add(elem)

    def __getitem__(self, item: tp.Union[(slice, int)]) -> tp.Union[(T, tp.Iterator[T])]:
        return self.items[item]

    def remove(self, other: T) -> None:
        """
        Remove an element from the list

        :param other: element to remove
        :raises ValueError: element not in list
        """
        index = self.items.index(other)
        del self.items[index]
        del self.keys[index]

    def add(self, other: T) -> int:
        """
        Add an element. Returns the index at which it was inserted.

        :param other: element to insert
        :return: index that the entry is available now at
        """
        key_value = self.key(other)
        for index in range(len(self.keys)):
            if key_value <= self.keys[index]:
                break
        else:
            index = len(self.keys)

        self.items.insert(index, other)
        self.keys.insert(index, key_value)
        return index


class SliceableDeque(collections.abc.MutableSequence, tp.Generic[T]):
    __doc__ = '\n    A collections.deque that supports slicing.\n\n    Just note that it will return a generator upon being sliced!\n    '
    __slots__ = ('deque', )

    def __bool__(self) -> bool:
        return bool(self.deque)

    def insert(self, i: int, item: T):
        self.deque.insert(i, item)

    def __init__(self, *args, **kwargs):
        self.deque = (collections.deque)(*args, **kwargs)

    def __setitem__(self, key: int, value: T) -> None:
        self.deque[key] = value

    def __delitem__(self, key: int) -> None:
        del self.deque[key]

    def __iter__(self) -> tp.Iterator[T]:
        return iter(self.deque)

    def __len__(self) -> int:
        return len(self.deque)

    def __reversed__(self) -> tp.Iterator[T]:
        return reversed(self.deque)

    def __contains__(self, item: T) -> bool:
        return item in self.deque

    def __getattr__(self, item: str):
        return getattr(self.deque, item)

    def __getitem__(self, item) -> tp.Union[(tp.Iterator[T], T)]:
        """Return either one element, or a generator over a slice"""
        tot_length = len(self)
        if type(item) is slice:
            start, stop, step = item.indices(tot_length)

            def generator():
                for index in range(start, stop, step):
                    yield self.deque[index]

            return generator()
        else:
            return self.deque[item]