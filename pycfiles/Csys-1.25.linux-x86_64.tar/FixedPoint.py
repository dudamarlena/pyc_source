# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/FixedPoint.py
# Compiled at: 2013-02-11 20:21:04
"""
FixedPoint objects support decimal arithmetic with a fixed number of
digits (called the object's precision) after the decimal point.  The
number of digits before the decimal point is variable & unbounded.

The precision is user-settable on a per-object basis when a FixedPoint
is constructed, and may vary across FixedPoint objects.  The precision
may also be changed after construction via FixedPoint.set_precision(p).
Note that if the precision of a FixedPoint is reduced via set_precision,
information may be lost to rounding.

>>> x = FixedPoint("5.55")  # precision defaults to 2
>>> print x
5.55
>>> x.set_precision(1)      # round to one fraction digit
>>> print x
5.6
>>> print FixedPoint("5.55", 1)  # same thing setting to 1 in constructor
5.6
>>> repr(x) #  returns constructor string that reproduces object exactly
"FixedPoint('5.6', 1)"
>>>

When FixedPoint objects of different precision are combined via + - * /,
the result is computed to the larger of the inputs' precisions, which also
becomes the precision of the resulting FixedPoint object.

>>> print FixedPoint("3.42") + FixedPoint("100.005", 3)
103.425
>>>

When a FixedPoint is combined with other numeric types (ints, floats,
strings representing a number) via + - * /, then similarly the computation
is carried out using-- and the result inherits --the FixedPoint's
precision.

>>> print FixedPoint(1) / 7
0.14
>>> print FixedPoint(1, 30) / 7
0.142857142857142857142857142857
>>>

The string produced by str(x) (implictly invoked by "print") always
contains at least one digit before the decimal point, followed by a
decimal point, followed by exactly x.get_precision() digits.  If x is
negative, str(x)[0] == "-".

The FixedPoint constructor can be passed an int, long, string, float,
FixedPoint, or any object convertible to a float via float() or to a
long via long().  Passing a precision is optional; if specified, the
precision must be a non-negative int.  There is no inherent limit on
the size of the precision, but if very very large you'll probably run
out of memory.

Note that conversion of floats to FixedPoint can be surprising, and
should be avoided whenever possible.  Conversion from string is exact
(up to final rounding to the requested precision), so is greatly
preferred.

>>> print FixedPoint(1.1e30)
1099999999999999993725589651456.00
>>> print FixedPoint("1.1e30")
1100000000000000000000000000000.00
>>>

The following Python operators and functions accept FixedPoints in the
expected ways:

    binary + - * / % divmod
        with auto-coercion of other types to FixedPoint.
        + - % divmod  of FixedPoints are always exact.
        * / of FixedPoints may lose information to rounding, in
            which case the result is the infinitely precise answer
            rounded to the result's precision.
        divmod(x, y) returns (q, r) where q is a long equal to
            floor(x/y) as if x/y were computed to infinite precision,
            and r is a FixedPoint equal to x - q * y; no information
            is lost.  Note that q has the sign of y, and abs(r) < abs(y).
    unary -
    == != < > <= >=  cmp
    min  max
    float  int  long    (int and long truncate)
    abs
    str  repr
    hash
    use as dict keys
    use as boolean (e.g. "if some_FixedPoint:" -- true iff not zero)

Methods unique to FixedPoints:
   .copy()              return new FixedPoint with same value
   .frac()              long(x) + x.frac() == x
   .get_precision()
   .set_precision(p)
"""
__version__ = (
 0, 0, 4)
DEFAULT_PRECISION = 2

class FixedPoint():

    def __init__(self, value=0, precision=DEFAULT_PRECISION):
        self.n = self.p = 0
        self.set_precision(precision)
        p = self.p
        if isinstance(value, type('42.3e5')):
            n, exp = _string2exact(value)
            effective_exp = exp + p
            if effective_exp > 0:
                n = n * _tento(effective_exp)
            elif effective_exp < 0:
                n = _roundquotient(n, _tento(-effective_exp))
            self.n = n
            return
        if isinstance(value, type(42)) or isinstance(value, type(42)):
            self.n = long(value) * _tento(p)
            return
        if isinstance(value, FixedPoint):
            temp = value.copy()
            temp.set_precision(p)
            self.n, self.p = temp.n, temp.p
            return
        if isinstance(value, type(42.0)):
            import math
            f, e = math.frexp(abs(value))
            assert f == 0 or 0.5 <= f < 1.0
            CHUNK = 28
            top = 0
            while f:
                f = math.ldexp(f, CHUNK)
                digit = int(f)
                assert digit >> CHUNK == 0
                top = top << CHUNK | digit
                f = f - digit
                assert 0.0 <= f < 1.0
                e = e - CHUNK

            top = top * _tento(p)
            if e >= 0:
                n = top << e
            else:
                n = _roundquotient(top, 1 << -e)
            if value < 0:
                n = -n
            self.n = n
            return
        if isinstance(value, type(complex(42.0, -42.0))):
            raise TypeError("can't convert complex to FixedPoint: " + `value`)
        yes = 1
        try:
            asfloat = float(value)
        except:
            yes = 0

        if yes:
            self.__init__(asfloat, p)
            return
        yes = 1
        try:
            aslong = long(value)
        except:
            yes = 0

        if yes:
            self.__init__(aslong, p)
            return
        raise TypeError("can't convert to FixedPoint: " + `value`)

    def get_precision(self):
        """Return the precision of this FixedPoint.

           The precision is the number of decimal digits carried after
           the decimal point, and is an int >= 0.
        """
        return self.p

    def set_precision(self, precision=DEFAULT_PRECISION):
        """Change the precision carried by this FixedPoint to p.

           precision must be an int >= 0, and defaults to
           DEFAULT_PRECISION.

           If precision is less than this FixedPoint's current precision,
           information may be lost to rounding.
        """
        try:
            p = int(precision)
        except:
            raise TypeError('precision not convertable to int: ' + `precision`)

        if p < 0:
            raise ValueError('precision must be >= 0: ' + `precision`)
        if p > self.p:
            self.n = self.n * _tento(p - self.p)
        elif p < self.p:
            self.n = _roundquotient(self.n, _tento(self.p - p))
        self.p = p

    def __str__(self):
        n, p = self.n, self.p
        i, f = divmod(abs(n), _tento(p))
        if p:
            frac = repr(f)[:-1]
            frac = '0' * (p - len(frac)) + frac
        else:
            frac = ''
        return '-'[:n < 0] + repr(i)[:-1] + '.' + frac

    def __repr__(self):
        return 'FixedPoint' + `(str(self), self.p)`

    def copy(self):
        return _mkFP(self.n, self.p)

    __copy__ = __deepcopy__ = copy

    def __cmp__(self, other):
        xn, yn, p = _norm(self, other)
        return cmp(xn, yn)

    def __hash__(self):
        n, p = self.__reduce()
        return hash(n) ^ hash(p)

    def __nonzero__(self):
        return self.n != 0

    def __neg__(self):
        return _mkFP(-self.n, self.p)

    def __abs__(self):
        if self.n >= 0:
            return self.copy()
        else:
            return -self

    def __add__(self, other):
        n1, n2, p = _norm(self, other)
        return _mkFP(n1 + n2, p)

    __radd__ = __add__

    def __sub__(self, other):
        if not isinstance(other, FixedPoint):
            other = FixedPoint(other, self.p)
        return self.__add__(-other)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        n1, n2, p = _norm(self, other)
        return _mkFP(_roundquotient(n1 * n2, _tento(p)), p)

    __rmul__ = __mul__

    def __div__(self, other):
        n1, n2, p = _norm(self, other)
        if n2 == 0:
            raise ZeroDivisionError('FixedPoint division')
        if n2 < 0:
            n1, n2 = -n1, -n2
        return _mkFP(_roundquotient(n1 * _tento(p), n2), p)

    def __rdiv__(self, other):
        n1, n2, p = _norm(self, other)
        return _mkFP(n2, p) / self

    def __divmod__(self, other):
        n1, n2, p = _norm(self, other)
        if n2 == 0:
            raise ZeroDivisionError('FixedPoint modulo')
        q = n1 / n2
        return (
         q, _mkFP(n1 - q * n2, p))

    def __rdivmod__(self, other):
        n1, n2, p = _norm(self, other)
        return divmod(_mkFP(n2, p), self)

    def __mod__(self, other):
        return self.__divmod__(other)[1]

    def __rmod__(self, other):
        n1, n2, p = _norm(self, other)
        return _mkFP(n2, p).__mod__(self)

    def __float__(self):
        n, p = self.__reduce()
        return float(n) / float(_tento(p))

    def __long__(self):
        answer = abs(self.n) / _tento(self.p)
        if self.n < 0:
            answer = -answer
        return answer

    def __int__(self):
        return int(self.__long__())

    def frac(self):
        """Return fractional portion as a FixedPoint.

           x.frac() + long(x) == x
        """
        return self - long(self)

    def __reduce(self):
        n, p = self.n, self.p
        if n == 0:
            p = 0
        while p and n % 10 == 0:
            p = p - 1
            n = n / 10

        return (
         n, p)


def _tento(n, cache={}):
    try:
        return cache[n]
    except KeyError:
        answer = cache[n] = 10 ** n
        return answer


def _norm(x, y, isinstance=isinstance, FixedPoint=FixedPoint, _tento=_tento):
    if not isinstance(x, FixedPoint):
        raise AssertionError
        y = isinstance(y, FixedPoint) or FixedPoint(y, x.p)
    xn, yn = x.n, y.n
    xp, yp = x.p, y.p
    if xp > yp:
        yn = yn * _tento(xp - yp)
        p = xp
    elif xp < yp:
        xn = xn * _tento(yp - xp)
        p = yp
    else:
        p = xp
    return (
     xn, yn, p)


def _mkFP(n, p, FixedPoint=FixedPoint):
    f = FixedPoint()
    f.n = n
    f.p = p
    return f


def _roundquotient(x, y):
    assert y > 0
    n, leftover = divmod(x, y)
    c = cmp(leftover << 1, y)
    if c > 0 or c == 0 and n & 1 == 1:
        n = n + 1
    return n


import re
_parser = re.compile('\n    \\s*\n    (?P<sign>[-+])?\n    (\n        (?P<int>\\d+) (\\. (?P<frac>\\d*))?\n    |\n        \\. (?P<onlyfrac>\\d+)\n    )\n    ([eE](?P<exp>[-+]? \\d+))?\n    \\s* $\n', re.VERBOSE).match
del re

def _string2exact(s):
    m = _parser(s)
    if m is None:
        raise ValueError("can't parse as number: " + `s`)
    exp = m.group('exp')
    if exp is None:
        exp = 0
    else:
        exp = int(exp)
    intpart = m.group('int')
    if intpart is None:
        intpart = '0'
        fracpart = m.group('onlyfrac')
    else:
        fracpart = m.group('frac')
        if fracpart is None or fracpart == '':
            fracpart = '0'
    assert intpart
    assert fracpart
    i, f = long(intpart), long(fracpart)
    nfrac = len(fracpart)
    i = i * _tento(nfrac) + f
    exp = exp - nfrac
    if m.group('sign') == '-':
        i = -i
    return (i, exp)


def _test():
    fp = FixedPoint
    o = fp('0.1')
    assert str(o) == '0.10'
    t = fp('-20e-2', 5)
    assert str(t) == '-0.20000'
    assert t < o
    assert o > t
    assert min(o, t) == min(t, o) == t
    assert max(o, t) == max(t, o) == o
    assert o != t
    assert --t == t
    assert abs(t) > abs(o)
    assert abs(o) < abs(t)
    assert o == o and t == t
    assert t.copy() == t
    assert o == -t / 2 == -0.5 * t
    assert abs(t) == o + o
    assert abs(o) == o
    assert o / t == -0.5
    assert -(t / o) == -t / o == t / -o == 2
    assert 1 + o == o + 1 == fp(' +00.000011e+5  ')
    assert 1 / o == 10
    assert o + t == t + o == -o
    assert 2.0 * t == t * 2 == '2' * t == o / o * 2 * t
    assert 1 - t == -(t - 1) == fp(6) / 5
    assert t * t == 4 * o * o == o * 4 * o == o * o * 4
    assert fp(2) - '1' == 1
    assert float(-1 / t) == 5.0
    for p in range(20):
        assert 42 + fp('1e-20', p) - 42 == 0

    assert 1 / (42 + fp('1e-20', 20) - 42) == fp('100.0E18')
    o = fp('.9995', 4)
    assert 1 - o == fp('5e-4', 10)
    o.set_precision(3)
    assert o == 1
    o = fp('.9985', 4)
    o.set_precision(3)
    assert o == fp('.998', 10)
    assert o == o.frac()
    o.set_precision(100)
    assert o == fp('.998', 10)
    o.set_precision(2)
    assert o == 1
    x = fp(1.99)
    assert long(x) == -long(-x) == 1
    assert int(x) == -int(-x) == 1
    assert x == long(x) + x.frac()
    assert -x == long(-x) + (-x).frac()
    assert fp(7) % 4 == 7 % fp(4) == 3
    assert fp(-7) % 4 == -7 % fp(4) == 1
    assert fp(-7) % -4 == -7 % fp(-4) == -3
    assert fp(7.0) % '-4.0' == 7 % fp(-4) == -1
    assert fp('5.5') % fp('1.1') == fp('5.5e100') % fp('1.1e100') == 0
    assert divmod(fp('1e100'), 3) == (long(fp('1e100') / 3), 1)


if __name__ == '__main__':
    _test()