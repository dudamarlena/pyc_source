# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/weakutil.py
# Compiled at: 2018-01-06 14:43:43
import warnings
from weakref import ref
from assertutil import precondition

class WeakMethod:
    """ Wraps a function or, more importantly, a bound method, in
    a way that allows a bound method's object to be GC'd """

    def __init__(self, fn, callback=None):
        warnings.warn('deprecated', DeprecationWarning)
        precondition(hasattr(fn, 'im_self'), 'fn is required to be a bound method.')
        self._cleanupcallback = callback
        self._obj = ref(fn.im_self, self.call_cleanup_cb)
        self._meth = fn.im_func

    def __call__(self, *args, **kws):
        s = self._obj()
        if s:
            return self._meth(s, *args, **kws)

    def __repr__(self):
        return '<%s %s %s>' % (self.__class__.__name__, self._obj, self._meth)

    def call_cleanup_cb(self, thedeadweakref):
        if self._cleanupcallback is not None:
            self._cleanupcallback(self, thedeadweakref)
        return


def factory_function_name_here(o):
    if hasattr(o, 'im_self'):
        return WeakMethod(o)
    else:
        return o