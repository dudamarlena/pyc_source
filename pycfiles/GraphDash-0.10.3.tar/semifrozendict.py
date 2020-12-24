# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: graphdash/struct/semifrozendict.py
# Compiled at: 2019-04-25 09:26:58
from __future__ import print_function, unicode_literals

class SemiFrozenDict(dict):
    """
    This is an implementation of a dict who blocks
    new keys after initialization, but allows for
    existing keys to be modified.

    The use case is if you have configuration that
    needs to be overriden.
    """

    def __setitem__(self, key, value):
        if key in self:
            super(SemiFrozenDict, self).__setitem__(key, value)
        else:
            print((b'(!) Preventing addition of new key "{0}" in dict, authorized keys are {1}').format(key, list(self)))

    def update(self, *args, **kwargs):
        dict_ = dict(*args, **kwargs)
        for k in dict_:
            self[k] = dict_[k]