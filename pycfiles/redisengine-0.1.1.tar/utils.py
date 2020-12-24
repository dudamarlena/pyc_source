# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/joekavalieri/git/conversionman/conversionman/lib/python2.7/site-packages/redisengine/utils.py
# Compiled at: 2016-03-19 04:56:37
try:
    from django.utils.functional import cached_property
except ImportError:

    class cached_property(object):
        """
        Decorator that converts a method with a single self argument into a
        property cached on the instance.

        Optional ``name`` argument allows you to make cached properties of other
        methods. (e.g.  url = cached_property(get_absolute_url, name='url') )
        """

        def __init__(self, func, name=None):
            self.func = func
            self.__doc__ = getattr(func, '__doc__')
            self.name = name or func.__name__

        def __get__(self, instance, type=None):
            if instance is None:
                return self
            else:
                res = instance.__dict__[self.name] = self.func(instance)
                return res