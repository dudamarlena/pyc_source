# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tinyaspect.py
# Compiled at: 2008-08-24 07:05:47
import logging, aspects
from peak.util.decorators import decorate_class

class aspect_instance(object):

    def __init__(self, a, mode, args, kw):
        self.a = a
        self.mode = mode
        self.args = args
        self.kw = kw

    def wrap(self, f):

        def later(cls):
            self.cls = cls
            self.f = f
            if not self.mode == aspect.ATTACH:
                aspects.with_wrap(self.wrapper, getattr(cls, f.__name__))
            else:
                self.a(cls, f, *self.args, **self.kw)
            return cls

        decorate_class(later)
        return f

    def wrapper(self, *args, **kw):
        if self.mode == aspect.MODIFY:
            rv = yield aspects.proceed(*args, **kw)
            rv = self.a(rv, *self.args, **self.kw)
        elif self.mode == aspect.NORMAL:
            self.a(*self.args, **self.kw)
            rv = yield aspects.proceed(*args, **kw)
        yield aspects.return_stop(rv)


class aspect(object):
    NORMAL = 0
    MODIFY = 1
    ATTACH = 2

    def __init__(self, mode=NORMAL, attach=False):
        self.mode = mode

    def __call__(self, a):
        self.a = a
        return self.wrap

    def wrap(self, *args, **kw):
        return aspect_instance(self.a, self.mode, args, kw).wrap