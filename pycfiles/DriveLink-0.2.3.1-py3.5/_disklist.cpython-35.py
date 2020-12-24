# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drivelink/_disklist.py
# Compiled at: 2017-09-04 20:22:31
# Size of source mod 2**32: 4902 bytes
from collections import MutableSequence
from os.path import expanduser, join
from drivelink import Link

class List(Link, MutableSequence):
    __doc__ = '\n    A list class that maintains O(k) look up and O(1) append while keeping RAM usage O(1) as well.\n    Unfortunately, insert is O(n/k).\n\n    This is accomplished through paging every size_limit consecutive values together\n    behind the scenes.\n\n    The object created can be used any way a normal list would be used, and will\n    clean itself up on python closing. This means saving all the remaining pages\n    to disk. If the file_basename and file_location was used before, it will load\n    the old values back into itself so that the results can be reused.\n\n    There are two ways to initialize this object, as a standard object:\n\n        >>> diskList = List("samplelist")\n        >>> for i in range(10):\n        ...     diskList.append(i)\n        ...\n        >>> diskList[3]\n        3\n        >>> ", ".join(str(x) for x in diskList)\n        \'0, 1, 2, 3, 4, 5, 6, 7, 8, 9\'\n        >>> del diskList[5]\n        >>> ", ".join(str(x) for x in diskList)\n        \'0, 1, 2, 3, 4, 6, 7, 8, 9\'\n\n    Or through context:\n\n        >>> with List("testlist") as d:\n        ...     for i in range(10):\n        ...         d.append(i)\n        ...     print(d[3])\n        3\n\n    If there is a way to break list like behavior and you can reproduce it, please\n    report it to `the GitHub issues <https://github.com/cdusold/DriveLink/issues/>`_.\n    '

    def __init__(self, file_basename, size_limit=1024, max_pages=16, file_location=join(expanduser('~'), '.DriveLink'), compression_ratio=0):
        self.pages = dict()
        self._number_of_pages = 0
        super(List, self).__init__(file_basename, size_limit, max_pages, file_location, compression_ratio)

    def copy_from(self, other):
        for value in other:
            self.append(value)

    def load_index(self):
        other_values = super(List, self).load_index()
        if other_values is None:
            return
        self._number_of_pages = other_values[0]

    def store_index(self):
        super(List, self).store_index(self._number_of_pages)

    def open_page(self, k):
        if 0 <= k < self._number_of_pages:
            self._load_page_from_disk(k)
        else:
            raise IndexError

    def determine_index(self, key):
        """
        Figures out where the key in question should be.
        """
        if key < 0:
            key += self._length
        return divmod(key, self.size_limit)

    def page_indices(self):
        for k in range(self._number_of_pages):
            yield k

    def __delitem__(self, key):
        """
         Deletes the key value in question from the pages.
        """
        super(List, self).__delitem__(key)
        i, _ = self.determine_index(key)
        for i in range(i, self._number_of_pages - 1):
            self.open_page(i + 1)
            if self.pages[(i + 1)]:
                v = self.pages[(i + 1)][0]
                del self.pages[(i + 1)][0]
                self.pages[i].append(v)
                self._guarantee_page(i + 1)

        self._guarantee_page(self._number_of_pages - 1)
        if not self.pages[(self._number_of_pages - 1)]:
            del self.pages[self._number_of_pages - 1]
            self._number_of_pages -= 1

    def __reversed__(self):
        for p in reversed(range(self._number_of_pages)):
            self._guarantee_page(p)
            for i in reversed(self.pages[p]):
                yield i

    def page_removed(self, number):
        self._number_of_pages -= 1

    def __str__(self):
        return 'List with values stored to ' + self._file_base

    def append(self, v):
        k = self._length // self.size_limit
        if k == self._number_of_pages:
            self._newpage()
        self._guarantee_page(k)
        self.pages[k].append(v)
        self._length += 1

    def insert(self, i, v):
        k, i = divmod(i, self.size_limit)
        if k == self._number_of_pages:
            self._newpage()
        self._guarantee_page(k)
        self.pages[k].insert(i, v)
        if len(self.pages[k]) > self.size_limit:
            for k in range(k, self._number_of_pages - 1):
                self._guarantee_page(k)
                v = self.pages[k][(-1)]
                del self.pages[k][-1]
                self._guarantee_page(k + 1)
                self.pages[(k + 1)].insert(0, v)

            if len(self.pages[(self._number_of_pages - 1)]) > self.size_limit:
                self._newpage()
                self.pages[(self._number_of_pages - 1)].append(self.pages[(self._number_of_pages - 2)][(-1)])
                del self.pages[(self._number_of_pages - 2)][-1]
        self._length += 1

    def _newpage(self):
        self.pages[self._number_of_pages] = []
        self._queue.append(self._number_of_pages)
        self._number_of_pages += 1