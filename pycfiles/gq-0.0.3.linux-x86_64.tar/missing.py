# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ganow/.pyenv/versions/gq-test/lib/python2.7/site-packages/gq/missing.py
# Compiled at: 2015-03-02 04:01:19


class MethodMissing(object):

    def __getattr__(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:

            def method(*args, **kw):
                return self.method_missing(name, *args, **kw)

            return method

    def method_missing(self, name, *args, **kw):
        raise AttributeError('%r object has no attribute %r' % (
         self.__class__, name))


class ValMissing(object):

    def __getattr__(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:
            return self.val_missing(name)

    def val_missing(self, name):
        raise AttributeError('%r object has no attribute %r' % (
         self.__class__, name))