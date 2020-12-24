# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/evnet/util.py
# Compiled at: 2011-02-27 10:25:24
import collections, weakref

class EventGen(object):

    def __init__(self):
        self._event_subscribers = collections.defaultdict(list)

    def _on(self, name, cb):
        self._event_subscribers[name].append(cb)

    def _event(self, name, *args):
        for cb in self._event_subscribers[name]:
            cb(*args)


class WeakMethodBound:

    def __init__(self, f):
        self.f = f.im_func
        self.c = weakref.ref(f.im_self)

    def __call__(self, *args):
        if self.c() == None:
            raise TypeError, 'Method called on dead object'
        apply(self.f, (self.c(),) + args)
        return

    def alive(self):
        return not self.c() == None


class WeakMethodFree:

    def __init__(self, f):
        self.f = weakref.ref(f)

    def __call__(self, *args):
        if self.f() == None:
            raise TypeError, 'Function no longer exist'
        apply(self.f(), args)
        return

    def alive(self):
        return not self.f() == None


def WeakMethod(f):
    try:
        f.im_func
    except AttributeError:
        return WeakMethodFree(f)

    return WeakMethodBound(f)