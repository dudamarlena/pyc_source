# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-fat3/egg/alacarte/util.py
# Compiled at: 2010-03-18 05:47:02
__all__ = [
 'Cache']

class Cache(dict):
    """A least-recently-used (LRU) cache.
    
    Discards the least recently referenced object when full.
    
    Based on Python Cookbook contributions from multiple sources:
    
        * http://code.activestate.com/recipes/521871/
        * http://code.activestate.com/recipes/498110/
        * http://code.activestate.com/recipes/252524/
        * http://code.activestate.com/recipes/498245/
    
    And Genshi's LRUCache:
    
        http://genshi.edgewall.org/browser/trunk/genshi/util.py
    
    Warning: If memory cleanup is diabled this dictionary will leak.
    
    """

    class CacheElement(object):

        def __init__(self, key, value):
            self.previous = self.next = None
            self.key, self.value = key, value
            return

        def __repr__(self):
            return repr(self.value).replace('object at', 'proxy object at')

    def __init__(self, capacity):
        super(Cache, self).__init__()
        self.head = self.tail = None
        self.capacity = capacity
        return

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.key
            cur = cur.next

    def __getitem__(self, key):
        element = super(Cache, self).__getitem__(key)
        self._update(element)
        return element.value

    def __setitem__(self, key, value):
        try:
            element = super(Cache, self).__getitem__(key)
            element.value = value
            self._update(element)
        except KeyError:
            element = self.CacheElement(key, value)
            super(Cache, self).__setitem__(key, element)
            self._insert(element)

        self._restrict()

    def _insert(self, element):
        element.previous, element.next = None, self.head
        if self.head is not None:
            self.head.previous = element
        else:
            self.tail = element
        self.head = element
        return

    def _restrict(self):
        while len(self) > self.capacity:
            del self[self.tail.key]
            if self.tail != self.head:
                self.tail = self.tail.previous
                self.tail.next = None
            else:
                self.head = self.tail = None

        return

    def _update(self, element):
        if self.head == element:
            return
        else:
            previous = element.previous
            previous.next = element.next
            if element.next is not None:
                element.next.previous = previous
            else:
                self.tail = previous
            element.previous, element.next = None, self.head
            self.head.previous = self.head = element
            return