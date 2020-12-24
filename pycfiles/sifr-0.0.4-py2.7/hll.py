# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/sifr/hll.py
# Compiled at: 2015-06-10 09:00:02
from hyperloglog import HyperLogLog

class HLLCounter(object):

    def __init__(self):
        """
        Simple counter that uses hyperloglog
        to count unique occurrences per key
        """
        self.counter = {}

    def pop(self, key):
        """
        Removes a key from the counter
        :param key:
        """
        self.counter.pop(key, None)
        return

    def add(self, key, identifier):
        """
        Adds a key to the counter
        :param key:
        :param identifier: any object that can be represented
         as a string
        """
        self.counter.setdefault(key, HyperLogLog(0.005))
        self.counter[key].add(str(identifier))

    def get(self, key):
        """
        Gets the unique occurrences in the set
        :param key:
        """
        if key not in self.counter:
            return 0
        return int(self.counter[key].card())