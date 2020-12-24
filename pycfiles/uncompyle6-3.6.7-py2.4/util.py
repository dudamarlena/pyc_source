# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/util.py
# Compiled at: 2020-04-27 23:06:35
try:
    from math import copysign

    def is_negative_zero(n):
        """Returns true if n is -0.0"""
        return n == 0.0 and copysign(1, n) == -1


except:

    def is_negative_zero(n):
        return False


from uncompyle6 import PYTHON_VERSION

def better_repr(v, version):
    """Work around Python's unorthogonal and unhelpful repr() for primitive float
    and complex."""
    if isinstance(v, float):
        if str(v) in frozenset(['nan', '-nan', 'inf', '-inf']):
            return "float('%s')" % v
        elif is_negative_zero(v):
            return '-0.0'
        return repr(v)
    elif isinstance(v, complex):
        real = better_repr(v.real, version)
        imag = better_repr(v.imag, version)
        return 'complex(%s, %s)' % (real, imag)
    elif isinstance(v, tuple):
        if len(v) == 1:
            return '(%s,)' % better_repr(v[0], version)
        return '(%s)' % (', ').join((better_repr(i, version) for i in v))
    elif PYTHON_VERSION < 3.0 and isinstance(v, long):
        s = repr(v)
        if version >= 3.0 and s[(-1)] == 'L':
            return s[:-1]
        else:
            return s
    elif isinstance(v, list):
        l = better_repr(v)
        if len(v) == 1:
            return '[%s,]' % better_repr(v[0], version)
        return '[%s]' % (', ').join((better_repr(i) for i in v))
    else:
        return repr(v)