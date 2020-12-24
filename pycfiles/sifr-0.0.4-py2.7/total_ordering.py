# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/sifr/backports/total_ordering.py
# Compiled at: 2015-06-10 09:00:02
"""
total_ordering backport from http://code.activestate.com/recipes/576685/
"""

def total_ordering(cls):
    """Class decorator that fills-in missing ordering methods"""
    convert = {'__lt__': [
                (
                 '__gt__', lambda self, other: other < self),
                (
                 '__le__', lambda self, other: not other < self),
                (
                 '__ge__', lambda self, other: not self < other)], 
       '__le__': [
                (
                 '__ge__', lambda self, other: other <= self),
                (
                 '__lt__', lambda self, other: not other <= self),
                (
                 '__gt__', lambda self, other: not self <= other)], 
       '__gt__': [
                (
                 '__lt__', lambda self, other: other > self),
                (
                 '__ge__', lambda self, other: not other > self),
                (
                 '__le__', lambda self, other: not self > other)], 
       '__ge__': [
                (
                 '__le__', lambda self, other: other >= self),
                (
                 '__gt__', lambda self, other: not other >= self),
                (
                 '__lt__', lambda self, other: not self >= other)]}
    if hasattr(object, '__lt__'):
        roots = [ op for op in convert if getattr(cls, op) is not getattr(object, op) ]
    else:
        roots = set(dir(cls)) & set(convert)
    assert roots, 'must define at least one ordering operation: < > <= >='
    root = max(roots)
    for opname, opfunc in convert[root]:
        if opname not in roots:
            opfunc.__name__ = opname
            opfunc.__doc__ = getattr(int, opname).__doc__
            setattr(cls, opname, opfunc)

    return cls