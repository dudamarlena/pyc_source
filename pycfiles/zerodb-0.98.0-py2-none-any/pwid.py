# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/catalog/indexes/pwid.py
# Compiled at: 2016-04-22 11:29:50
import persistent
from zope.index.text import widcode

class PersistentWid(persistent.Persistent):
    """
    Behaves like a string, but stored as a lazy-loaded persistent object.
    Can be encoded from word ids
    """

    def __init__(self, s):
        self.s = s

    @classmethod
    def encode_wid(cls, l):
        return cls(widcode.encode(l))

    def decode_wid(self):
        return widcode.decode(self.s)

    def __getattribute__(self, attr):
        try:
            return super(PersistentWid, self).__getattribute__(attr)
        except AttributeError:
            return super(PersistentWid, self).__getattribute__('s').__getattribute__(attr)