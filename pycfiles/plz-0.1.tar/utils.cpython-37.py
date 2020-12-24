# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pybasic/utils.py
# Compiled at: 2019-03-30 10:08:30
# Size of source mod 2**32: 1208 bytes


class Stack:

    def __init__(self, items=[]):
        self.items = items

    def __len__(self):
        return len(self.items)

    def top(self):
        return self.items[(-1)]

    def push(self, x):
        self.items.append(x)

    def pop(self):
        return self.items.pop()


class RootStack(Stack):
    control_blocks = ('<WHILE>', '<DO>', '<FOR>')
    closure_blocks = ('<SUB>', '<FUNCTION>')

    def control_top(self):
        for item in reversed(self.items):
            if item.parent.value in RootStack.control_blocks:
                return item

    def closure_top(self):
        for item in reversed(self.items):
            if item.parent.value in RootStack.closure_blocks:
                return item


class BasicError(Exception):
    pass


def item_getter(x):

    def getter(args):
        result = x
        for layer in args:
            basic_count = layer.run()
            py_count = basic_count - 1
            try:
                result = result[py_count]
            except IndexError:
                raise BasicError('Index %d is out of range (maximum %d)' % (basic_count, len(result)))

        return result

    return getter