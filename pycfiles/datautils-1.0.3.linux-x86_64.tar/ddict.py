# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/graham/.virtualenvs/temcagt/lib/python2.7/site-packages/datautils/ddict/ddict.py
# Compiled at: 2013-12-13 14:50:04
"""
'Dotted' dictionary access (similar to pymongo sub-document addressing)

With a dict d,

d = {'a': {'b': 1}}

Normally, to access 'b's value you would run

d['a']['b']

which can be cumbersome for large document heirarchies.
These utilities are meant to allow for access like this

dget(d, 'a.b')
"""
from ops import dget, dset, ddel

class DDict(dict):
    """
    Allow getting, setting and deleting of nested dictionaries
    like those returned from a MongoDB using a '.' notation.

    Example
    -------
    d = DotAddressed({'a': {'b': {'c': 1}}})
    d['a.b.c']  # 1
    del d['a.b.c']  # {'a': {'b': {}}}
    d['a.b'] = 2  # {'a': {'b': 2}}
    """

    def __getitem__(self, key):
        if '.' not in key:
            return dict.__getitem__(self, key)
        return dget(self, key)

    def __setitem__(self, key, value):
        if '.' not in key:
            dict.__setitem__(self, key, value)
        else:
            dset(self, key, value)

    def __delitem__(self, key):
        if '.' not in key:
            return dict.__delitem__(self, key)
        ddel(self, key)

    def get(self, key, default=None):
        try:
            i = self[key]
            return i
        except KeyError:
            return default