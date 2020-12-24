# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gg/PycharmProjects/gg-python3-crdt/build/lib/src/gset.py
# Compiled at: 2019-04-22 02:28:32
# Size of source mod 2**32: 614 bytes


class GSet:

    def __init__(self, id):
        self.payload = []
        self.id = id

    def add(self, elem):
        self.payload.append(elem)
        self.payload.sort()

    def query(self, elem):
        return elem in self.payload

    def compare(self, gs2):
        for elem in self.payload:
            if elem not in gs2.payload:
                return False

        return True

    def merge(self, gs2):
        for elem in gs2.payload:
            if elem not in self.payload:
                self.payload.append(elem)

        self.payload.sort()

    def display(self):
        print(self.payload)