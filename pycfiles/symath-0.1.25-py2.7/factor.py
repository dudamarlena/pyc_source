# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/symath/factor.py
# Compiled at: 2015-08-21 11:58:24
import symath, memoize

@memoize.Memoize
def is_factor(x, y):
    """
  return True if x is a factor of y
  will return True for any 2 numbers because we use floating point
  """
    a, b = symath.wilds('a b')
    val = symath.WildResults()
    if x == y:
        return True
    else:
        if isinstance(x, symath.Number) and isinstance(y, symath.Number):
            return True
        if y.match(a * b, val):
            return is_factor(x, val.a) or is_factor(x, val.b)
        if y.match(a + b, val):
            return is_factor(x, val.a) and is_factor(x, val.b)
        if y.match(a - b, val):
            return is_factor(x, val.a) and is_factor(x, val.b)
        return False


@memoize.Memoize
def get_coefficient(y, x):
    """
  divides y by x and returns
  - only works if x is a factor of y
  """
    assert is_factor(x, y)
    assert x != 1
    a, b, c = symath.wilds('a b c')
    val = symath.WildResults()
    if y == x:
        return symath.symbolic(1)
    if y.match(a * b, val):
        if is_factor(x, val.a):
            return get_coefficient(val.a, x) * val.b
        else:
            return get_coefficient(val.b, x) * val.a

    elif y.match(c(a, b), val):
        return val.c(get_coefficient(val.a, x), get_coefficient(val.b, x))