# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/util/nbest_list.py
# Compiled at: 2014-11-06 01:53:55


class NBestList(object):

    def __init__(self, N, reverse=False):
        self.N = N
        self._list = []
        self._count = 0
        self._reverse = reverse

    def add(self, score, item):
        """
        Add an item with score.
        :param item: item
        :param score: score
        """
        self._list.append((score, item))
        self._count += 1
        if len(self._list) > self.N and len(self._list) > self._count / 10:
            self._list.sort(reverse=not self._reverse)
            del self._list[self.N:len(self._list)]

    def get(self):
        """
        Get result.
        :rtype: list of (float, score)
        """
        self._list.sort(reverse=not self._reverse)
        if len(self._list) > self.N:
            del self._list[self.N:len(self._list)]
        return self._list

    def get_copy(self):
        """
        Get a copy of result.
        :rtype: list of (float, score)
        """
        return list(self.get())

    def is_empty(self):
        """
        Is empty.
        :rtype: bool
        """
        return len(self._list) == 0