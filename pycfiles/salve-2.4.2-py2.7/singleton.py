# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/class_resources/singleton.py
# Compiled at: 2015-11-06 23:45:35


class Singleton(type):
    """
    A metaclass for making classes Singletons.

    Example usage:

    >>> class A(object):
    >>>     __metaclass__ = Singleton
    >>>     def __init__(self, a, b):
    >>>         self.a = a
    >>>         self.b = b
    >>> x = A(1,2)
    >>> repr(x)
    <A object at 0x7fe6a76d8510>
    >>> y = A(1,2)
    >>> repr(y)
    '<A object at 0x7fe6a76d8510>'

    However, note that Singletons ignore the arguments that they are given for
    subsequent constructions. That means that we can have a somewhat
    unexpected result when trying to get another instance of A:

    >>> z = A('abc', 'def')
    >>> repr(z)
    '<A object at 0x7fe6a76d8510>'
    """

    def __call__(cls, *args, **kwargs):
        """
        Redefine class construction to start by looking for an instance of the
        class to return and returning it if found
        """
        try:
            instance = cls._instance
        except AttributeError:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
            instance = cls._instance

        return instance