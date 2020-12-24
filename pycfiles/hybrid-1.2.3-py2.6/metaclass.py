# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hybrid/metaclass.py
# Compiled at: 2016-01-10 07:55:56
import string, types, traceback, tornado

class CatchExceptionMeta(type):

    def __new__(mcs, cls_name, bases, attrs):
        supported_methods = map(string.lower, tornado.web.RequestHandler.SUPPORTED_METHODS)
        for attr in attrs:
            if attr in supported_methods and isinstance(attrs[attr], types.FunctionType):
                attrs[attr] = CatchExceptionMeta.catch(attrs[attr])

        return type.__new__(mcs, cls_name, bases, attrs)

    @staticmethod
    def catch(f):

        def _inner(self, *a, **kw):
            try:
                return f(self, *a, **kw)
            except Exception, _:
                self.set_status(500)
                self.write(traceback.format_exc())
                self.finish()

        return _inner