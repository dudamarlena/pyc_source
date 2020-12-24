# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/marrow/util/insensitive.py
# Compiled at: 2012-07-26 02:07:58
"""A dictionary with case-insensitive access."""
from marrow.util.object import NoDefault
__all__ = [
 'CaseInsensitiveDict']

class CaseInsensitiveDict(dict):

    def __init__(self, default=None, *args, **kw):
        self._o = {}
        if default is None:
            default = dict()
            default.update(kw)
        for i in default:
            self[i] = default[i]

        super(CaseInsensitiveDict, self).__init__()
        return

    def items(self):
        return [ (self._o[k], self[k]) for k in self ]

    def __setitem__(self, k, v):
        try:
            nk = k.lower()
        except:
            nk = k

        self._o[nk] = k
        super(CaseInsensitiveDict, self).__setitem__(nk, v)

    def __getitem__(self, k):
        try:
            nk = k.lower()
        except:
            nk = k

        return super(CaseInsensitiveDict, self).__getitem__(nk)