# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/whooshdoc/epyhacks.py
# Compiled at: 2009-02-22 19:29:03
""" Hacks for to help epydoc read certain packages.
"""
from epydoc import docintrospecter

def type_name_predicate(type_module, type_name):
    """ Return a predicate function that returns True if an object is a strict
    instance of a type given by its module and name.

    Instances of subclasses are not considered.
    """

    def f(obj):
        typ = type(obj)
        return getattr(typ, '__module__', None) == type_module and getattr(typ, '__name__', None) == type_name

    return f


def register_hacks():
    """ Register hacks for special cases.
    """
    docintrospecter.register_introspecter(type_name_predicate('numpy', 'ufunc'), docintrospecter.introspect_routine)
    docintrospecter.register_introspecter(type_name_predicate('__builtin__', 'fortran'), docintrospecter.introspect_routine)