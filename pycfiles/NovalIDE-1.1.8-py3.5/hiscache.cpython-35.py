# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/util/hiscache.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 7805 bytes
"""
NovalIDE Buisness Model Library: HistoryCache

History cache that acts as a stack for managing a history list o

"""
__all__ = [
 'HistoryCache', 'HIST_CACHE_UNLIMITED',
 'CycleCache']
HIST_CACHE_UNLIMITED = -1

class HistoryCache(object):
    __doc__ = 'Data management cache.\n    Maintains a positional list of objects that remembers the last access \n    position in the cache.\n\n    '

    def __init__(self, max_size=HIST_CACHE_UNLIMITED):
        """@param max_size: size of history cache (int)"""
        super(HistoryCache, self).__init__()
        self._list = list()
        self.cpos = -1
        self.max_size = max_size

    def _Resize(self):
        """Adjust cache size based on max size setting"""
        if self.max_size != HIST_CACHE_UNLIMITED:
            lsize = len(self._list)
            if lsize:
                adj = self.max_size - lsize
                if adj < 0:
                    self._list.pop(0)
                    self.cpos = len(self._list) - 1

    def __getitem__(self, index):
        return self._list[index]

    def Clear(self):
        """Clear the history cache"""
        del self._list
        self._list = list()
        self.cpos = -1

    def GetSize(self):
        """Get the current size of the cache
        @return: int (number of items in the cache)

        """
        return len(self._list)

    def GetMaxSize(self):
        """Get the max size of the cache
        @return: int

        """
        return self.max_size

    def GetNextItem(self):
        """Get the next item in the history cache, moving the
        current position towards the end of the cache.
        @return: object or None if at end of list

        """
        item = None
        if self.cpos < len(self._list) - 1:
            self.cpos += 1
            item = self._list[self.cpos]
        return item

    def GetPreviousItem(self):
        """Get the previous item in the history cache, moving the
        current position towards the beginning of the cache.
        @return: object or None if at start of list

        """
        item = None
        if self.cpos >= 0 and len(self._list) > 0:
            if self.cpos == len(self._list):
                self.cpos -= 1
            item = self._list[self.cpos]
            self.cpos -= 1
        return item

    def HasPrevious(self):
        """Are there more items to the left of the current position
        @return: bool

        """
        llen = len(self._list)
        more = self.cpos >= 0 and llen and self.cpos < llen
        return more

    def HasNext(self):
        """Are there more items to the right of the current position
        @return: bool

        """
        if self.cpos == -1 and len(self._list):
            more = True
        else:
            more = self.cpos >= 0 and self.cpos < len(self._list) - 1
        return more

    def PeekNext(self):
        """Return the next item in the cache without modifying the
        currently managed position.
        @return: cache object

        """
        if self.HasNext():
            return self._list[(self.cpos + 1)]
        else:
            return

    def PeekPrevious(self):
        """Return the previous item in the cache without modifying the
        currently managed position.
        @return: cache object

        """
        if self.HasPrevious():
            return self._list[self.cpos]
        else:
            return

    def PutItem(self, item):
        """Put an item on the top of the cache
        @param item: object

        """
        if self.cpos != len(self._list) - 1:
            if self.cpos < 0:
                self.cpos = 0
            self._list = self._list[:self.cpos + 1]
        self._list.append(item)
        self.cpos += 1
        self._Resize()

    def SetMaxSize(self, max_size):
        """Set the maximum size of the cache
        @param max_size: int (HIST_CACHE_UNLIMITED for unlimited size)

        """
        if not max_size > 0:
            assert max_size == 1, 'Invalid max size'
            self.max_size = max_size
            self._Resize()


class CycleCache(object):
    __doc__ = 'A simple circular cache. All items are added to the end of the cache\n    regardless of the current reference position. As items are accessed from\n    the cache the cache reference pointer is incremented, if it passes the\n    end it will go back to the beginning.\n\n    '
    TRIM_LAST = 1
    TRIM_FIRST = 2
    ADD_FIRST = 3
    ADD_LAST = 4

    def __init__(self, size, trim=TRIM_FIRST, add=ADD_LAST):
        """Initialize the cache.
        @param size: cache size

        """
        super(CycleCache, self).__init__()
        self._list = list()
        self._cpos = -1
        self._size = size
        self._trim = trim
        self._add = add

    def __len__(self):
        return len(self._list)

    def NextIndex(self):
        """Get the next index in the cache
        @return: int

        """
        idx = self._cpos
        idx -= 1
        if abs(idx) > len(self._list):
            idx = -1
        return idx

    def Clear(self):
        """Clear the cache"""
        del self._list
        self._list = list()

    def GetCurrentSize(self):
        """Get the size of the cache
        @return: int

        """
        return len(self._list)

    def GetNext(self):
        """Get the next item in the cache and increment the
        current position.
        @return: object

        """
        item = None
        if len(self._list):
            item = self._list[self._cpos]
            self._cpos = self.NextIndex()
        return item

    def PeekNext(self):
        """Look the next item in the cache
        @return: object

        """
        item = None
        if abs(self._cpos) < len(self._list):
            item = self._list[self._cpos]
        return item

    def PeekPrev(self):
        """Look the next item in the cache
        @return: object

        """
        idx = self._cpos + 1
        if idx == 0:
            idx = -1 * len(self._list)
        llen = len(self._list)
        if llen and abs(idx) <= llen:
            item = self._list[idx]
        else:
            item = None
        return item

    def PutItem(self, item):
        """Put an item in the cache
        @param item: object

        """
        llen = len(self._list)
        if llen and llen == self._size:
            if self._trim == self.TRIM_FIRST:
                del self._list[0]
            elif self._trim == self.TRIM_LAST:
                del self._list[self._size - 1]
            if self._add == self.ADD_LAST:
                self._list.append(item)
        elif self._add == self.ADD_FIRST:
            self._list.insert(0, item)

    def Reset(self):
        """Reset the list reference pointer"""
        self._cpos = -1