# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wb_vandalism/datasources/util.py
# Compiled at: 2015-11-17 10:14:31
# Size of source mod 2**32: 1078 bytes


class DictDiffer(object):
    __doc__ = '\n    Calculate the difference between two dictionaries as:\n    (1) items added\n    (2) items removed\n    (3) keys same in both but changed values\n    (4) keys same in both and unchanged values\n    \n    Copied from\n    http://stackoverflow.com/questions/1165352/calculate-difference-in-keys-contained-in-two-python-dictionaries\n    '

    def __init__(self, current_dict, past_dict=None):
        self.current_dict, self.past_dict = current_dict, past_dict or {}
        self.set_current = set(current_dict.keys())
        self.set_past = set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        return self.set_current - self.intersect

    def removed(self):
        return self.set_past - self.intersect

    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])