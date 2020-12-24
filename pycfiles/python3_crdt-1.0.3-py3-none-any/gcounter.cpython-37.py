# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gg/PycharmProjects/gg-python3-crdt/build/lib/src/gcounter.py
# Compiled at: 2019-04-22 02:28:32
# Size of source mod 2**32: 809 bytes


class GCounter:

    def __init__(self, id):
        self.payload = {}
        self.id = id

    def add_new_node(self, key):
        self.payload[key] = 0

    def inc(self, key):
        try:
            self.payload[key] += 1
        except Exception as e:
            try:
                print('{}'.format(e))
            finally:
                e = None
                del e

    def query(self):
        return sum(self.payload.values())

    def compare(self, gc2):
        for key in self.payload:
            if self.payload[key] > gc2.payload[key]:
                return False

    def merge(self, gc2):
        new_payload = {key:0 for key in self.payload}
        for key in self.payload:
            new_payload[key] = max(self.payload[key], gc2.payload[key])

        self.payload = new_payload

    def display(self):
        print(self.payload.values())