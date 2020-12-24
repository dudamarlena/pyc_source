# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/tokenquery/models/stack.py
# Compiled at: 2017-01-28 16:19:23
# Size of source mod 2**32: 490 bytes


class Stack:

    def __init__(self, items=[]):
        self.items = items

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def peek(self):
        if len(self.items) > 0:
            return self.items[(len(self.items) - 1)]
        else:
            return

    def size(self):
        return len(self.items)