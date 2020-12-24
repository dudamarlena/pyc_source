# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/symath/simplestruct.py
# Compiled at: 2015-08-21 11:58:24
from pprint import PrettyPrinter

class SimpleStruct(object):

    def __init__(self, **kargs):
        for k in kargs:
            setattr(self, k, kargs[k])

    def __to_dict__(self):
        rv = {}
        mems = [ k for k in dir(self) if k[:2] != '__' ]
        for k in mems:
            r = getattr(self, k)
            if type(r) == type(self):
                r = r.__to_dict__()
            rv[k] = r

        return rv

    def __str__(self):
        pp = PrettyPrinter()
        return pp.pformat(self.__to_dict__())

    def __repr__(self):
        return str(self)