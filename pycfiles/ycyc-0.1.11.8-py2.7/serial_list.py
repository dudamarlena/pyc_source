# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/ycollections/serial_list.py
# Compiled at: 2016-05-25 10:16:25
from ycyc.ycollections.heap import Heap

class SerialListItem(object):

    def __init__(self, sn, value):
        self.sn = sn
        self.value = value


class SerialList(object):

    def __init__(self, sn=0, reverse=False):
        self.next_sn = sn
        self.heap = Heap(cmp_attrs=['sn'], reverse=False)

    def push_item(self, item):
        self.heap.push(item)

    def push(self, sn, value):
        self.push_item(SerialListItem(sn, value))

    def pop_item(self, force=False):
        while True:
            items = self.heap.headn(1)
            if not items:
                break
            item = items[0]
            if item.sn < self.next_sn:
                self.heap.pop()
            else:
                if item.sn == self.next_sn or force:
                    item = self.heap.pop()
                    self.next_sn = item.sn + 1
                    return item
                break

        return

    def pop(self, force=False):
        item = self.pop_item(force)
        return item and item.value