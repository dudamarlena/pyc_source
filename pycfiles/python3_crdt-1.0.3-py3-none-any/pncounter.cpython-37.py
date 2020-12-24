# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gg/PycharmProjects/gg-python3-crdt/build/lib/src/pncounter.py
# Compiled at: 2019-04-22 02:28:32
# Size of source mod 2**32: 795 bytes
from gcounter import GCounter

class PNCounter:

    def __init__(self, id):
        self.P = GCounter(id)
        self.N = GCounter(id)
        self.id = id

    def add_new_node(self, key):
        self.P.add_new_node(key)
        self.N.add_new_node(key)

    def inc(self, key):
        self.P.inc(key)

    def dec(self, key):
        self.N.inc(key)

    def query(self):
        return self.P.query() - self.N.query()

    def compare(self, gc2):
        return self.P.compare(gc2.P) and self.N.compare(gc2.N)

    def merge(self, gc2):
        self.P.merge(gc2.P)
        self.N.merge(gc2.N)

    def display(self, name):
        print(('{}.P: '.format(name)), end='')
        self.P.display()
        print(('{}.N: '.format(name)), end='')
        self.N.display()