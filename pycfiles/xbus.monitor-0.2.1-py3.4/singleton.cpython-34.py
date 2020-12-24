# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/utils/singleton.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 804 bytes


class Singleton(type):
    __doc__ = "\n    This is a neat singleton pattern. This was found in a comment on this page:\n    http://www.garyrobinson.net/2004/03/python_singleto.html\n\n    to use this, example :\n    >>> class C(object):\n    ...     __metaclass__ = Singleton\n    ...     def __init__(self, foo):\n    ...         self.foo = foo\n\n    >>> C('bar').foo\n    'bar'\n\n    >>> C().foo\n    'bar'\n\n    and your class C is now a singleton, and it is safe to use the __init__\n    method as you usually do...\n    "

    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance = None

    def __call__(mcs, *args, **kw):
        if mcs.instance is None:
            mcs.instance = super(Singleton, mcs).__call__(*args, **kw)
        return mcs.instance