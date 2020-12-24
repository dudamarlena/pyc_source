# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hybrid/skeleton/project/controllers/base_handler.py
# Compiled at: 2016-02-02 23:06:14
from collections import Sequence
from tornado.web import RequestHandler
from hybrid.util import imports
from hybrid.metaclass import CatchExceptionMeta

class CastException(Exception):
    pass


class BaseHandler(RequestHandler):
    __metaclass__ = CatchExceptionMeta

    def getviewfunc(self, view, module):
        if not view and not module:
            from ..views import json_view
            return json_view
        if not view:
            raise RuntimeError('missing view function name')
        if not module:
            from .. import views
            m = views
        else:
            m = imports(module)
        if not m or not hasattr(m, view):
            raise RuntimeError("can't find %s:%s" % (module, view))
        return getattr(m, view)

    def render_func(self, data, view=None, module=None, *a, **kw):
        self.write(self.getviewfunc(view, module)(data, *a, **kw))
        self.finish()

    def cast(self, v, t):
        try:
            return t(v)
        except:
            return CastException()

    def param_check(self, args, howto=None):
        howto = howto or (lambda a: self.get_argument(a, None))
        for arg in args:
            arg = list(arg)
            if len(arg) == 1:
                arg += [(type,)]
            if len(arg) == 2:
                arg += [lambda *a, **kw: True]
            if not isinstance(arg[1], Sequence):
                arg[1] = (
                 arg[1],)
            else:
                arg[1] = tuple(arg[1])
            value = howto(arg[0])
            if value is None and None in arg[1]:
                continue
            elif value is None and None not in arg[1]:
                return False

            def __check(t):
                value2 = self.cast(value, t)
                if not isinstance(value2, CastException) and isinstance(value2, arg[1]) and arg[2](value2):
                    return True

            if not any([ __check(t) for t in arg[1] ]):
                return False

        return True