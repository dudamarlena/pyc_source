# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/skeletool/container.py
# Compiled at: 2012-08-31 11:30:16


class Container(object):

    @staticmethod
    def __new__(cls):
        if cls is Container:
            raise TypeError('Cannot directly instanciate ' + repr(cls))
        if '_instance' not in dir(cls):
            cls._instance = super(Container, cls).__new__(cls)
            cls._instance._items = {}
        return cls._instance

    def get(self, cls):
        if cls in self._items:
            return self._items[cls]
        else:
            return

    def set(self, item):
        self._items[item.__class__] = item

    def all(self):
        return self._items