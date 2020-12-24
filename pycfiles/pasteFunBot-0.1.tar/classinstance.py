# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/makina/pasteStage/pasteFunBot/Paste-1.7.2-py2.6.egg/paste/util/classinstance.py
# Compiled at: 2009-07-20 09:44:04


class classinstancemethod(object):
    """
    Acts like a class method when called from a class, like an
    instance method when called by an instance.  The method should
    take two arguments, 'self' and 'cls'; one of these will be None
    depending on how the method was called.
    """

    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__

    def __get__(self, obj, type=None):
        return _methodwrapper(self.func, obj=obj, type=type)


class _methodwrapper(object):

    def __init__(self, func, obj, type):
        self.func = func
        self.obj = obj
        self.type = type

    def __call__(self, *args, **kw):
        assert not kw.has_key('self') and not kw.has_key('cls'), "You cannot use 'self' or 'cls' arguments to a classinstancemethod"
        return self.func(*((self.obj, self.type) + args), **kw)

    def __repr__(self):
        if self.obj is None:
            return '<bound class method %s.%s>' % (
             self.type.__name__, self.func.func_name)
        else:
            return '<bound method %s.%s of %r>' % (
             self.type.__name__, self.func.func_name, self.obj)
            return