# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\weakmethod.py
# Compiled at: 2017-12-11 20:12:50
import weakref, sys
py3 = sys.version_info >= (3, 0)
try:
    from weakref import ReferenceError
except:
    pass

try:
    from weakref import WeakMethod
except ImportError:

    class WeakMethod(weakref.ref):
        """
        A custom `weakref.ref` subclass which simulates a weak reference to
        a bound method, working around the lifetime problem of bound methods.
        """
        __slots__ = ('_func_ref', '_meth_type', '_alive', '__weakref__')

        def __new__(cls, meth, callback=None):
            try:
                obj = meth.__self__
                func = meth.__func__
            except AttributeError:
                raise TypeError(('argument should be a bound method, not {}').format(type(meth)))

            def _cb(arg):
                self = self_wr()
                if self._alive:
                    self._alive = False
                    if callback is not None:
                        callback(self)
                return

            self = weakref.ref.__new__(cls, obj, _cb)
            self._func_ref = weakref.ref(func, _cb)
            self._meth_type = type(meth)
            self._alive = True
            self_wr = weakref.ref(self)
            return self

        if not py3:

            def __call__(self):
                obj = super(WeakMethod, self).__call__()
                func = self._func_ref()
                if obj is None or func is None:
                    return
                return self._meth_type(func, obj, type(obj))

        else:

            def __call__(self):
                obj = super(WeakMethod, self).__call__()
                func = self._func_ref()
                if obj is None or func is None:
                    return
                return self._meth_type(func, obj)

        def __eq__(self, other):
            if isinstance(other, WeakMethod):
                if not self._alive or not other._alive:
                    return self is other
                return ref.__eq__(self, other) and self._func_ref == other._func_ref
            return False

        def __ne__(self, other):
            if isinstance(other, WeakMethod):
                if not self._alive or not other._alive:
                    return self is not other
                return ref.__ne__(self, other) or self._func_ref != other._func_ref
            return True

        __hash__ = weakref.ref.__hash__


class WeakMethodProxy(object):
    """
    A weak proxy to a weak method.  Similar to weakref.proxy() but
    works with bound methods.  has a "fallback" argument, which replaces
    the target as a delegate when the target goes away.
    """

    def __init__(self, meth, callback=None, fallback=None):
        """
        Create a weak proxy to a bound method.  "callback" is called
        with this proxy as an argument when the underlying WeakMethod
        object goes stale.  "fallback" is then used as a delegate instead.
        """
        if callback:
            self_wr = weakref.ref(self)

            def _cb(arg):
                callback(self)

            self.weak_method = WeakMethod(meth, callback=_cb)
        else:
            self.weak_method = WeakMethod(meth)
        self.fallback = fallback

    def __call__(self, *args, **kwds):
        method = self.weak_method()
        if method:
            return method(*args, **kwds)
        if self.fallback:
            return self.fallback(*args, **kwds)
        raise ReferenceError('weakly-referenced object no longer exists')

    __hash__ = None

    def __repr__(self):
        return '<WeakMethodProxy at %d to %r>' % (id(self), self.weak_method())

    def __eq__(self, other):
        if isinstance(other, WeakMethodProxy):
            a, b = self.weak_method(), other.weak_method()
            if a is None or b is None:
                raise ReferenceError('weakly-referenced object no longer exists')
            return a == b
        else:
            return


def ref(obj, callback=None):
    """Create a weak reference, returning a WeakMethod if appropriate"""
    try:
        return WeakMethod(obj, callback)
    except TypeError:
        return weakref.ref(obj, callback)


def proxy(obj, callback=None, fallback=None):
    """Create a proxy, returning a WeakMethodProxy if appropriate"""
    try:
        return WeakMethodProxy(obj, callback, fallback)
    except TypeError:
        return weakref.proxy(obj, callback)