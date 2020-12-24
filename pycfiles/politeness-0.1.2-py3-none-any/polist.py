# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/polist/polist.py
# Compiled at: 2014-05-09 14:00:57
from collections import defaultdict

class PartialOrderedList(list):

    def __init__(self, values=[]):
        list.__init__(self)
        self.groups = []
        for value, group in values:
            list.append(self, value)
            self.groups.append(group)

    def __eq__(self, l):
        grouped = defaultdict(list)
        for i, group in enumerate(self.groups):
            grouped[group].append(list(self)[i])

        for e, group in zip(l, self.groups):
            if e in grouped[group]:
                grouped[group].remove(e)
            else:
                return False

        return True

    def __ne__(self, l):
        return not self.__eq__(l)

    def append(self, value, group):
        list.append(self, value)
        self.groups.append(group)