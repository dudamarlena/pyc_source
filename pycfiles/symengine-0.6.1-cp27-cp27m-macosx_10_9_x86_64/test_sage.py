# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/wheel/symengine/tests/test_sage.py
# Compiled at: 2020-03-16 01:41:57
from symengine import Integer, symbols, sin, cos, pi, E, I, oo, zoo, nan, true, false, Add, function_symbol, DenseMatrix, sympify, log, EulerGamma, Catalan, GoldenRatio
from symengine.lib.symengine_wrapper import PyNumber, PyFunction, sage_module, wrap_sage_function, LambertW, KroneckerDelta, erf, lowergamma, uppergamma, loggamma, beta, floor, ceiling, conjugate
import unittest
try:
    import sage.all
    have_sage = True
except ImportError:
    have_sage = False

@unittest.skipUnless(have_sage, 'Sage not installed')
def test_sage_conversions():
    x, y = sage.SR.var('x y')
    x1, y1 = symbols('x, y')
    assert x1._sage_() == x
    assert x1 == sympify(x)
    assert Integer(12)._sage_() == sage.Integer(12)
    assert Integer(12) == sympify(sage.Integer(12))
    assert (Integer(1) / 2)._sage_() == sage.Integer(1) / 2
    assert Integer(1) / 2 == sympify(sage.Integer(1) / 2)
    assert x1 + y == x1 + y1
    assert x1 * y == x1 * y1
    assert x1 ** y == x1 ** y1
    assert x1 - y == x1 - y1
    assert x1 / y == x1 / y1
    assert x + y1 == x + y
    assert x * y1 == x * y
    assert x - y1 == x - y
    assert x / y1 == x / y
    assert (x1 + y1)._sage_() == x + y
    assert (x1 * y1)._sage_() == x * y
    assert (x1 ** y1)._sage_() == x ** y
    assert (x1 - y1)._sage_() == x - y
    assert (x1 / y1)._sage_() == x / y
    assert x1 + y1 == sympify(x + y)
    assert x1 * y1 == sympify(x * y)
    assert x1 ** y1 == sympify(x ** y)
    assert x1 - y1 == sympify(x - y)
    assert x1 / y1 == sympify(x / y)
    assert sin(x1) == sin(x)
    assert sin(x1)._sage_() == sage.sin(x)
    assert sin(x1) == sympify(sage.sin(x))
    assert cos(x1) == cos(x)
    assert cos(x1)._sage_() == sage.cos(x)
    assert cos(x1) == sympify(sage.cos(x))
    assert function_symbol('f', x1, y1)._sage_() == sage.function('f', x, y)
    assert function_symbol('f', 2 * x1, x1 + y1).diff(x1)._sage_() == sage.function('f', 2 * x, x + y).diff(x)
    assert LambertW(x1) == LambertW(x)
    assert LambertW(x1)._sage_() == sage.lambert_w(x)
    assert KroneckerDelta(x1, y1) == KroneckerDelta(x, y)
    assert KroneckerDelta(x1, y1)._sage_() == sage.kronecker_delta(x, y)
    assert erf(x1) == erf(x)
    assert erf(x1)._sage_() == sage.erf(x)
    assert lowergamma(x1, y1) == lowergamma(x, y)
    assert lowergamma(x1, y1)._sage_() == sage.gamma_inc_lower(x, y)
    assert uppergamma(x1, y1) == uppergamma(x, y)
    assert uppergamma(x1, y1)._sage_() == sage.gamma_inc(x, y)
    assert loggamma(x1) == loggamma(x)
    assert loggamma(x1)._sage_() == sage.log_gamma(x)
    assert beta(x1, y1) == beta(x, y)
    assert beta(x1, y1)._sage_() == sage.beta(x, y)
    assert floor(x1) == floor(x)
    assert floor(x1)._sage_() == sage.floor(x)
    assert ceiling(x1) == ceiling(x)
    assert ceiling(x1)._sage_() == sage.ceil(x)
    assert conjugate(x1) == conjugate(x)
    assert conjugate(x1)._sage_() == sage.conjugate(x)
    assert pi._sage_() == sage.pi
    assert E._sage_() == sage.e
    assert I._sage_() == sage.I
    assert GoldenRatio._sage_() == sage.golden_ratio
    assert Catalan._sage_() == sage.catalan
    assert EulerGamma._sage_() == sage.euler_gamma
    assert oo._sage_() == sage.oo
    assert zoo._sage_() == sage.unsigned_infinity
    assert nan._sage_() == sage.NaN
    assert true._sage_() == True
    assert false._sage_() == False
    assert pi == sympify(sage.pi)
    assert E == sympify(sage.e)
    assert GoldenRatio == sympify(sage.golden_ratio)
    assert Catalan == sympify(sage.catalan)
    assert EulerGamma == sympify(sage.euler_gamma)
    assert oo == sympify(sage.oo)
    assert zoo == sympify(sage.unsigned_infinity)
    assert nan == sympify(sage.NaN)
    assert DenseMatrix(1, 2, [x1, y1])._sage_() == sage.matrix([[x, y]])
    a = sage.Mod(2, 7)
    b = PyNumber(a, sage_module)
    a = a + 8
    b = b + 8
    assert isinstance(b, PyNumber)
    assert b._sage_() == a
    a = a + x
    b = b + x
    assert isinstance(b, Add)
    assert b._sage_() == a
    e = x1 + wrap_sage_function(sage.log_gamma(x))
    assert str(e) == 'x + log_gamma(x)'
    assert isinstance(e, Add)
    assert e + wrap_sage_function(sage.log_gamma(x)) == x1 + 2 * wrap_sage_function(sage.log_gamma(x))
    f = e.subs({x1: 10})
    assert f == 10 + log(362880)
    f = e.subs({x1: 2})
    assert f == 2
    f = e.subs({x1: 100})
    v = f.n(53, real=True)
    assert abs(float(v) - 459.13420537) < 1e-07
    f = e.diff(x1)