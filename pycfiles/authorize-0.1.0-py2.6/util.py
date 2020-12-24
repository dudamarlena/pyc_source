# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-fat64/egg/authorize/util.py
# Compiled at: 2009-08-21 14:09:21
from authorize.gen_xml import base

def request(func):

    def req(self, **kw):
        args = func(**kw)
        return self.request(base(args[0], self.login, self.key, *args[1:]))

    req.__name__ = func.__name__
    req.func = func
    return req