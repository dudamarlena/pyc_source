# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gg/PycharmProjects/gg-python3-crdt/build/lib/src/twopset.py
# Compiled at: 2019-04-22 02:28:32
# Size of source mod 2**32: 672 bytes
from gset import GSet

class TwoPSet:

    def __init__(self, id):
        self.A = GSet(id)
        self.R = GSet(id)
        self.id = id

    def add(self, elem):
        self.A.add(elem)

    def remove(self, elem):
        self.R.add(elem)

    def query(self, elem):
        return self.A.query(elem) and not self.R.query(elem)

    def compare(self, tps2):
        return self.A.compare(tps2.A) and self.R.compare(tps2.R)

    def merge(self, tps2):
        self.A.merge(tps2.A)
        self.R.merge(tps2.R)

    def display(self):
        print('A: ', end='')
        self.A.display()
        print('R: ', end='')
        self.R.display()