# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parsimony/persistence/store.py
# Compiled at: 2014-11-30 18:27:57
# Size of source mod 2**32: 616 bytes
from abc import ABCMeta, abstractmethod

class Store(metaclass=ABCMeta):
    __doc__ = 'A store is an object that implements read and write capabilities for key-ed values\n\n    '

    def __init__(self, key):
        self.key = key

    @abstractmethod
    def read(self):
        """Method to retrieve the persisted value of this store.

        Must be overridden by subclasses.

        :return: the saved value from this store
        """
        pass

    @abstractmethod
    def write(self, value):
        """Method to persist a value in this store

        Must be overridden by subclasses.
        """
        pass