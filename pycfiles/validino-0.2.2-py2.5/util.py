# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/validino/util.py
# Compiled at: 2007-12-06 13:09:46
try:
    from functools import partial
except ImportError:

    def partial(func, *args, **kw):

        def inner(*_args, **_kw):
            d = kw.copy()
            d.update(_kw)
            return func(*(args + _args), **d)

        return inner