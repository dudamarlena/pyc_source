# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/util/classinstance.py
# Compiled at: 2012-02-27 07:41:58


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