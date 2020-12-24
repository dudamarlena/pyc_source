# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynhost/dynamic.py
# Compiled at: 2015-07-19 13:25:12
# Size of source mod 2**32: 789 bytes


class DynamicAction:

    def __init__(self):
        pass

    def evaluate(self, rule_match):
        pass


class Num(DynamicAction):

    def __init__(self, index=0, integer=True, default=0):
        self.index = index
        self.integer = integer
        self.default = default
        self.change = 0

    def evaluate(self, rule_match):
        try:
            num = int(rule_match.nums[self.index]) + self.change
        except IndexError:
            num = self.default

        if self.integer:
            return num
        return str(num)

    def add(self, n):
        self.change += n
        return self

    def multiply(self, n):
        self.change *= n
        return self


class RepeatCommand(DynamicAction):

    def __init__(self, count=1):
        self.count = count