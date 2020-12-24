# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\superpy\core\DataStructures.py
# Compiled at: 2010-06-04 07:07:11
"""Module containing various data structures used in superpy
"""

class NamedQueue:
    """A queue to track named elements.
    """

    def __init__(self):
        self._itemList = []
        self._itemDict = {}

    def Push(self, name, item):
        """Push a new named item in to the queue.
        
        INPUTS:
        
        -- name:        String name of new item.
        
        -- item:        Object representing the item.
        """
        if item is None:
            raise Exception('Cannot insert None into named queue.')
        if name in self._itemDict:
            raise Exception("Can't add item %s when item with that name is in queue." % name)
        else:
            self._itemList.append(name)
            self._itemDict[name] = item
        return

    def PopItem(self, name):
        """Remove the named item from the queue.
        
        INPUTS:
        
        -- name:        String name of item to remove.
        
        -------------------------------------------------------
        
        RETURNS:        Item with the given name.
        
        -------------------------------------------------------
        
        PURPOSE:        Pull the item with the given name out of the queue.
        
        """
        item = self._itemDict.get(name, None)
        if item is None:
            raise KeyError('No item named %s exists in this queue.\nContents:\n%s' % (
             str(name), ('\n').join(self._itemDict.keys())))
        itemIndex = self._itemList.index(name)
        self._itemList.pop(itemIndex)
        del self._itemDict[name]
        return item

    def __getitem__(self, name):
        return self._itemDict[name]

    def ShowItems(self):
        """Return sequence representing (name, item) for all items in queue.

        Items are returned in order they were put into the queue.
        """
        return [ (name, self._itemDict[name]) for name in self._itemList ]

    @staticmethod
    def _regr_test():
        """
>>> import DataStructures
>>> q = DataStructures.NamedQueue()
>>> q.Push('1',1)
>>> q.Push('2',2)
>>> q.Push('3',3)
>>> q.ShowItems()
[('1', 1), ('2', 2), ('3', 3)]
>>> q.PopItem('2')
2
>>> q.ShowItems()
[('1', 1), ('3', 3)]
        """
        pass


def _test():
    """Test docstrings in module."""
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()
    print 'Test finished.'