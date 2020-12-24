# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chartit\utils.py
# Compiled at: 2016-09-11 22:31:24
from collections import defaultdict

def _convert_to_rdd(obj):
    """Accepts a dict or a list of dicts and converts it to a
    RecursiveDefaultDict."""
    if isinstance(obj, dict):
        rdd = RecursiveDefaultDict()
        for k, v in obj.items():
            rdd[k] = _convert_to_rdd(v)

        return rdd
    if isinstance(obj, list):
        rddlst = []
        for ob in obj:
            rddlst.append(_convert_to_rdd(ob))

        return rddlst
    return obj


class RecursiveDefaultDict(defaultdict):
    """The name says it all.
    """

    def __init__(self, data=None):
        self.default_factory = type(self)
        if data is not None:
            self.data = _convert_to_rdd(data)
            self.update(self.data)
            del self.data
        return

    def __getitem__(self, key):
        return super(RecursiveDefaultDict, self).__getitem__(key)

    def __setitem__(self, key, item):
        if not isinstance(item, RecursiveDefaultDict):
            super(RecursiveDefaultDict, self).__setitem__(key, _convert_to_rdd(item))
        else:
            super(RecursiveDefaultDict, self).__setitem__(key, item)

    def update(self, element):
        super(RecursiveDefaultDict, self).update(_convert_to_rdd(element))