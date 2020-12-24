# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/folz/DFKI/Hacks/augpy/test/test_math.py
# Compiled at: 2020-03-09 10:20:54
# Size of source mod 2**32: 19865 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, random
from math import log
import numpy as np, pytest, augpy
from augpy.numeric_limits import CAST_LIMITS
from _common import I_TYPES
from _common import F_TYPES
from _common import TYPES
from _common import safe_cast
from _common import is_int
from _common import dtype_info
SIZE = (2, 178, 347)

def ind_rand_percentage(arr, pct):
    ind = np.linspace(0, 1, arr.size)
    np.random.shuffle(ind)
    return ind.reshape(arr.shape) <= pct


def _random_tensor(dtype, size=SIZE, ttype=None, default_vmin=-128, default_vmax=127):
    if ttype is None:
        ttype = augpy.to_temp_dtype(dtype)
    else:
        info = dtype_info(dtype)
        mu = 0
        sigma = log(info.max - mu)
        if info.min == 0:
            mu = 3
        if size == ():
            rand = np.random.normal(mu, sigma, 1)[0]
        else:
            rand = np.random.normal(mu, sigma, size)
            if is_int(dtype):
                rand[ind_rand_percentage(rand, 0.01)] = info.min
                rand[ind_rand_percentage(rand, 0.01)] = info.max
            rand = rand.clip(info.min, info.max)
        rand = rand.astype(dtype)
        if size is ():
            if rand == 0:
                rand = dtype(1)
        else:
            rand[rand == 0] = 1
    return (
     augpy.array_to_tensor(rand), rand.astype(ttype))


def _random_scalar(dtype):
    ttype = augpy.to_temp_dtype(dtype)
    vmin, vmax = CAST_LIMITS[(ttype, dtype)]
    vmin = vmin or 0
    vmax = vmax or 255
    s = random.random() * (vmax - vmin) + vmin
    if s == 0:
        return 1
    else:
        return s


def __random(fa, fn, close_allowed=False, rtol=1e-06, atol=1e-08, size1=SIZE, size2=None, size3=None):
    if size2 is None:
        size2 = size1
    for ctype, ntype in TYPES:
        c, a = _random_tensor(ntype, size1)
        d, b = _random_tensor(ntype, size2)
        if size3 is None:
            augpy_result = fa(c, d).numpy()
        else:
            result = augpy.CudaTensor(size3, dtype=ctype)
            fa(c, d, result)
            augpy_result = result.numpy()
        numpy_result = safe_cast(fn(a, b), ntype)
        augpy.default_stream.synchronize()
        if close_allowed:
            if is_int(ntype):
                atol = 1
            @py_assert1 = np.isclose
            @py_assert7 = @py_assert1(augpy_result, numpy_result, rtol=rtol, atol=atol)
            @py_assert9 = @py_assert7.all
            @py_assert11 = @py_assert9()
            if not @py_assert11:
                @py_format13 = (@pytest_ar._format_assertmsg(ctype) + '\n>assert %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py3)s, %(py4)s, rtol=%(py5)s, atol=%(py6)s)\n}.all\n}()\n}') % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(augpy_result) if 'augpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy_result) else 'augpy_result',  'py4':@pytest_ar._saferepr(numpy_result) if 'numpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(numpy_result) else 'numpy_result',  'py5':@pytest_ar._saferepr(rtol) if 'rtol' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rtol) else 'rtol',  'py6':@pytest_ar._saferepr(atol) if 'atol' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(atol) else 'atol',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format13))
            @py_assert1 = @py_assert7 = @py_assert9 = @py_assert11 = None
        else:
            @py_assert1 = augpy_result == numpy_result
            @py_assert5 = @py_assert1.all
            @py_assert7 = @py_assert5()
            if not @py_assert7:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (augpy_result, numpy_result)) % {'py0':@pytest_ar._saferepr(augpy_result) if 'augpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy_result) else 'augpy_result',  'py2':@pytest_ar._saferepr(numpy_result) if 'numpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(numpy_result) else 'numpy_result'}
                @py_format9 = (@pytest_ar._format_assertmsg(ctype) + '\n>assert %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.all\n}()\n}') % {'py4':@py_format3,  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert1 = @py_assert5 = @py_assert7 = None


def __random_scalar(fa, fn, close_allowed=False, rtol=1e-06, atol=1e-08, size=SIZE):
    for ctype, ntype in TYPES:
        a, n = _random_tensor(ntype, size)
        s = _random_scalar(ntype)
        augpy_result = fa(a, s).numpy()
        numpy_result = safe_cast(fn(n, s), ntype)
        augpy.default_stream.synchronize()
        if close_allowed:
            @py_assert1 = np.isclose
            @py_assert7 = @py_assert1(augpy_result, numpy_result, rtol=rtol, atol=atol)
            @py_assert9 = @py_assert7.all
            @py_assert11 = @py_assert9()
            if not @py_assert11:
                @py_format13 = (@pytest_ar._format_assertmsg(ctype) + '\n>assert %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py3)s, %(py4)s, rtol=%(py5)s, atol=%(py6)s)\n}.all\n}()\n}') % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(augpy_result) if 'augpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy_result) else 'augpy_result',  'py4':@pytest_ar._saferepr(numpy_result) if 'numpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(numpy_result) else 'numpy_result',  'py5':@pytest_ar._saferepr(rtol) if 'rtol' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rtol) else 'rtol',  'py6':@pytest_ar._saferepr(atol) if 'atol' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(atol) else 'atol',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format13))
            @py_assert1 = @py_assert7 = @py_assert9 = @py_assert11 = None
        else:
            @py_assert1 = augpy_result == numpy_result
            @py_assert5 = @py_assert1.all
            @py_assert7 = @py_assert5()
            if not @py_assert7:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (augpy_result, numpy_result)) % {'py0':@pytest_ar._saferepr(augpy_result) if 'augpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy_result) else 'augpy_result',  'py2':@pytest_ar._saferepr(numpy_result) if 'numpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(numpy_result) else 'numpy_result'}
                @py_format9 = (@pytest_ar._format_assertmsg(ctype) + '\n>assert %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.all\n}()\n}') % {'py4':@py_format3,  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert1 = @py_assert5 = @py_assert7 = None


def __random_unary(fa, fn, close_allowed=False, rtol=1e-06, atol=1e-08, size=SIZE, cast=True):
    for ctype, ntype in TYPES:
        a, n = _random_tensor(ntype, size)
        augpy_result = fa(a).numpy()
        numpy_result = fn(n)
        if cast:
            numpy_result = safe_cast(numpy_result, ntype)
        augpy.default_stream.synchronize()
        if close_allowed:
            @py_assert1 = np.isclose
            @py_assert7 = @py_assert1(augpy_result, numpy_result, rtol=rtol, atol=atol)
            @py_assert9 = @py_assert7.all
            @py_assert11 = @py_assert9()
            if not @py_assert11:
                @py_format13 = (@pytest_ar._format_assertmsg(ctype) + '\n>assert %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py3)s, %(py4)s, rtol=%(py5)s, atol=%(py6)s)\n}.all\n}()\n}') % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(augpy_result) if 'augpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy_result) else 'augpy_result',  'py4':@pytest_ar._saferepr(numpy_result) if 'numpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(numpy_result) else 'numpy_result',  'py5':@pytest_ar._saferepr(rtol) if 'rtol' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rtol) else 'rtol',  'py6':@pytest_ar._saferepr(atol) if 'atol' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(atol) else 'atol',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format13))
            @py_assert1 = @py_assert7 = @py_assert9 = @py_assert11 = None
        else:
            @py_assert1 = augpy_result == numpy_result
            @py_assert5 = @py_assert1.all
            @py_assert7 = @py_assert5()
            if not @py_assert7:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (augpy_result, numpy_result)) % {'py0':@pytest_ar._saferepr(augpy_result) if 'augpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy_result) else 'augpy_result',  'py2':@pytest_ar._saferepr(numpy_result) if 'numpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(numpy_result) else 'numpy_result'}
                @py_format9 = (@pytest_ar._format_assertmsg(ctype) + '\n>assert %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.all\n}()\n}') % {'py4':@py_format3,  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert1 = @py_assert5 = @py_assert7 = None


def __infix_random_scalar(fn, scalar, close_allowed=False):
    for ctype, ntype in TYPES:
        a, n = _random_tensor(ntype)
        a1 = fn(a, scalar).numpy()
        a2 = fn(scalar, a).numpy()
        n1 = safe_cast(fn(n, scalar), ntype)
        n2 = safe_cast(fn(scalar, n), ntype)
        augpy.default_stream.synchronize()
        if close_allowed:
            @py_assert1 = np.isclose
            @py_assert5 = 1e-06
            @py_assert7 = @py_assert1(a1, n1, rtol=@py_assert5)
            @py_assert9 = @py_assert7.all
            @py_assert11 = @py_assert9()
            if not @py_assert11:
                @py_format13 = (@pytest_ar._format_assertmsg(ctype) + '\n>assert %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py3)s, %(py4)s, rtol=%(py6)s)\n}.all\n}()\n}') % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(a1) if 'a1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a1) else 'a1',  'py4':@pytest_ar._saferepr(n1) if 'n1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n1) else 'n1',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format13))
            @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
            @py_assert1 = np.isclose
            @py_assert5 = 1e-06
            @py_assert7 = @py_assert1(a2, n2, rtol=@py_assert5)
            @py_assert9 = @py_assert7.all
            @py_assert11 = @py_assert9()
            if not @py_assert11:
                @py_format13 = (@pytest_ar._format_assertmsg(ctype) + '\n>assert %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py3)s, %(py4)s, rtol=%(py6)s)\n}.all\n}()\n}') % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(a2) if 'a2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a2) else 'a2',  'py4':@pytest_ar._saferepr(n2) if 'n2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n2) else 'n2',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format13))
            @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
        else:
            @py_assert1 = a1 == n1
            @py_assert5 = @py_assert1.all
            @py_assert7 = @py_assert5()
            if not @py_assert7:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (a1, n1)) % {'py0':@pytest_ar._saferepr(a1) if 'a1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a1) else 'a1',  'py2':@pytest_ar._saferepr(n1) if 'n1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n1) else 'n1'}
                @py_format9 = (@pytest_ar._format_assertmsg(ctype) + '\n>assert %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.all\n}()\n}') % {'py4':@py_format3,  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert1 = @py_assert5 = @py_assert7 = None
            @py_assert1 = a2 == n2
            @py_assert5 = @py_assert1.all
            @py_assert7 = @py_assert5()
            if not @py_assert7:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (a2, n2)) % {'py0':@pytest_ar._saferepr(a2) if 'a2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a2) else 'a2',  'py2':@pytest_ar._saferepr(n2) if 'n2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n2) else 'n2'}
                @py_format9 = (@pytest_ar._format_assertmsg(ctype) + '\n>assert %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.all\n}()\n}') % {'py4':@py_format3,  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert1 = @py_assert5 = @py_assert7 = None


def __infix_random_tensor(fn, close_allowed=False, rtol=1e-06, atol=1e-08):
    for ctype, ntype in TYPES:
        a1, n1 = _random_tensor(ntype)
        a2, n2 = _random_tensor(ntype)
        ra1 = fn(a1, a2).numpy()
        ra2 = fn(a2, a1).numpy()
        rn1 = safe_cast(fn(n1, n2), ntype)
        rn2 = safe_cast(fn(n2, n1), ntype)
        augpy.default_stream.synchronize()
        if close_allowed:
            @py_assert1 = np.isclose
            @py_assert7 = @py_assert1(ra1, rn1, rtol=rtol, atol=atol)
            @py_assert9 = @py_assert7.all
            @py_assert11 = @py_assert9()
            if not @py_assert11:
                @py_format13 = (@pytest_ar._format_assertmsg(ctype) + '\n>assert %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py3)s, %(py4)s, rtol=%(py5)s, atol=%(py6)s)\n}.all\n}()\n}') % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(ra1) if 'ra1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ra1) else 'ra1',  'py4':@pytest_ar._saferepr(rn1) if 'rn1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rn1) else 'rn1',  'py5':@pytest_ar._saferepr(rtol) if 'rtol' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rtol) else 'rtol',  'py6':@pytest_ar._saferepr(atol) if 'atol' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(atol) else 'atol',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format13))
            @py_assert1 = @py_assert7 = @py_assert9 = @py_assert11 = None
            @py_assert1 = np.isclose
            @py_assert7 = @py_assert1(ra2, rn2, rtol=rtol, atol=atol)
            @py_assert9 = @py_assert7.all
            @py_assert11 = @py_assert9()
            if not @py_assert11:
                @py_format13 = (@pytest_ar._format_assertmsg(ctype) + '\n>assert %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py3)s, %(py4)s, rtol=%(py5)s, atol=%(py6)s)\n}.all\n}()\n}') % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(ra2) if 'ra2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ra2) else 'ra2',  'py4':@pytest_ar._saferepr(rn2) if 'rn2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rn2) else 'rn2',  'py5':@pytest_ar._saferepr(rtol) if 'rtol' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rtol) else 'rtol',  'py6':@pytest_ar._saferepr(atol) if 'atol' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(atol) else 'atol',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format13))
            @py_assert1 = @py_assert7 = @py_assert9 = @py_assert11 = None
        else:
            @py_assert1 = ra1 == rn1
            @py_assert5 = @py_assert1.all
            @py_assert7 = @py_assert5()
            if not @py_assert7:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (ra1, rn1)) % {'py0':@pytest_ar._saferepr(ra1) if 'ra1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ra1) else 'ra1',  'py2':@pytest_ar._saferepr(rn1) if 'rn1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rn1) else 'rn1'}
                @py_format9 = (@pytest_ar._format_assertmsg(ctype) + '\n>assert %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.all\n}()\n}') % {'py4':@py_format3,  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert1 = @py_assert5 = @py_assert7 = None
            @py_assert1 = ra2 == rn2
            @py_assert5 = @py_assert1.all
            @py_assert7 = @py_assert5()
            if not @py_assert7:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (ra2, rn2)) % {'py0':@pytest_ar._saferepr(ra2) if 'ra2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ra2) else 'ra2',  'py2':@pytest_ar._saferepr(rn2) if 'rn2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rn2) else 'rn2'}
                @py_format9 = (@pytest_ar._format_assertmsg(ctype) + '\n>assert %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.all\n}()\n}') % {'py4':@py_format3,  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert1 = @py_assert5 = @py_assert7 = None


def test_infix_add_scalar():
    __infix_random_scalar(lambda a, b: a + b, 10)


def test_infix_add_tensor():
    __infix_random_tensor(lambda a, b: a + b)


def test_infix_sub_scalar():
    __infix_random_scalar(lambda a, b: a - b, 10)


def test_infix_sub_tensor():
    __infix_random_tensor(lambda a, b: a - b)


def test_infix_mul_scalar():
    __infix_random_scalar(lambda a, b: a * b, 10)


def test_infix_mul_tensor():
    __infix_random_tensor(lambda a, b: a * b)


def test_infix_div_scalar():
    __infix_random_scalar((lambda a, b: a / b), 10, close_allowed=True)


def test_infix_div_tensor():
    __infix_random_tensor((lambda a, b: a / b), close_allowed=True, atol=1)


def test_fma():
    ctype = augpy.float32
    ntype = np.float32
    result = augpy.CudaTensor((10, 10), dtype=ctype)
    a = np.arange(100, dtype=ntype).reshape((10, 10)).astype(ntype)
    b = np.arange(100, dtype=ntype).reshape((10, 10)).astype(ntype)
    c = augpy.array_to_tensor(a)
    d = augpy.array_to_tensor(b)
    s = 2
    augpy.fma(s, c, d, result)
    result_array = augpy.tensor_to_array(result)
    augpy.default_stream.synchronize()
    @py_assert2 = s * a
    @py_assert4 = @py_assert2 + b
    @py_assert5 = @py_assert4 == result_array
    @py_assert9 = @py_assert5.all
    @py_assert11 = @py_assert9()
    if not @py_assert11:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('((%(py0)s * %(py1)s) + %(py3)s) == %(py6)s', ), (@py_assert4, result_array)) % {'py0':@pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's',  'py1':@pytest_ar._saferepr(a) if 'a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a) else 'a',  'py3':@pytest_ar._saferepr(b) if 'b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(b) else 'b',  'py6':@pytest_ar._saferepr(result_array) if 'result_array' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result_array) else 'result_array'}
        @py_format13 = 'assert %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s.all\n}()\n}' % {'py8':@py_format7,  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert9 = @py_assert11 = None


def test_add():
    __random(augpy.add, lambda a, b: a + b)


def test_sub():
    __random(augpy.sub, lambda a, b: a - b)


def test_mul():
    __random(augpy.mul, lambda a, b: a * b)


def test_div():
    __random((augpy.div), (lambda a, b: a / b), close_allowed=True, atol=1)


def test_mul1d():
    for num in range(1, 100001, 3456):
        __random((augpy.mul), (lambda a, b: a * b), size1=(num,))


def test_add_scalar():
    __random_scalar(augpy.add, lambda a, b: a + b)


def test_sub_scalar():
    __random_scalar(augpy.sub, lambda a, b: a - b)


def test_mul_scalar():
    __random_scalar(augpy.mul, lambda a, b: a * b)


def test_div_scalar():
    __random_scalar((augpy.div), (lambda a, b: a / b), close_allowed=True)


def test_mmul_float():
    a = augpy.array_to_tensor(np.asarray([[1, 2, 3], [4, 5, 6]], np.float32))
    b = augpy.array_to_tensor(np.asarray([[7, 8], [9, 10], [11, 12]], np.float32))
    c = augpy.array_to_tensor(np.zeros((2, 2), np.float32))
    augpy.gemm(a, b, c, 1.0, 0.0)
    augpy_result = c.numpy()
    augpy.default_stream.synchronize()
    @py_assert1 = np.all
    @py_assert6 = np.asarray
    @py_assert8 = [
     [
      58, 64], [139, 154]]
    @py_assert11 = np.float32
    @py_assert13 = @py_assert6(@py_assert8, @py_assert11)
    @py_assert4 = augpy_result == @py_assert13
    @py_assert17 = @py_assert1(@py_assert4)
    if not @py_assert17:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s == %(py14)s\n{%(py14)s = %(py7)s\n{%(py7)s = %(py5)s.asarray\n}(%(py9)s, %(py12)s\n{%(py12)s = %(py10)s.float32\n})\n}', ), (augpy_result, @py_assert13)) % {'py3':@pytest_ar._saferepr(augpy_result) if 'augpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy_result) else 'augpy_result',  'py5':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py10':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format19 = 'assert %(py18)s\n{%(py18)s = %(py2)s\n{%(py2)s = %(py0)s.all\n}(%(py16)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py16':@py_format15,  'py18':@pytest_ar._saferepr(@py_assert17)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert17 = None


def test_mmul_float2():
    a = np.random.rand(100, 20).astype(np.float32)
    b = np.random.rand(20, 300).astype(np.float32)
    c = augpy.array_to_tensor(np.zeros((100, 300), np.float32))
    t_a = augpy.array_to_tensor(a)
    t_b = augpy.array_to_tensor(b)
    augpy.gemm(t_a, t_b, c, 1.0, 0.0)
    augpy_result = c.numpy()
    numpy_result = np.matmul(a, b)
    augpy.default_stream.synchronize()
    @py_assert1 = np.sum
    @py_assert4 = np.absolute
    @py_assert8 = augpy_result - numpy_result
    @py_assert9 = @py_assert4(@py_assert8)
    @py_assert11 = @py_assert1(@py_assert9)
    @py_assert13 = 100
    @py_assert15 = 300
    @py_assert17 = @py_assert13 * @py_assert15
    @py_assert18 = @py_assert11 / @py_assert17
    @py_assert20 = 1e-06
    @py_assert19 = @py_assert18 < @py_assert20
    if not @py_assert19:
        @py_format22 = @pytest_ar._call_reprcompare(('<', ), (@py_assert19,), ('(%(py12)s\n{%(py12)s = %(py2)s\n{%(py2)s = %(py0)s.sum\n}(%(py10)s\n{%(py10)s = %(py5)s\n{%(py5)s = %(py3)s.absolute\n}((%(py6)s - %(py7)s))\n})\n} / (%(py14)s * %(py16)s)) < %(py21)s', ), (@py_assert18, @py_assert20)) % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(augpy_result) if 'augpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy_result) else 'augpy_result',  'py7':@pytest_ar._saferepr(numpy_result) if 'numpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(numpy_result) else 'numpy_result',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15),  'py21':@pytest_ar._saferepr(@py_assert20)}
        @py_format24 = 'assert %(py23)s' % {'py23': @py_format22}
        raise AssertionError(@pytest_ar._format_explanation(@py_format24))
    @py_assert1 = @py_assert4 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert18 = @py_assert19 = @py_assert20 = None


def test_cast():
    for ctype, ntype in TYPES:
        for ctype_target, ntype_target in TYPES:
            a, n = _random_tensor(ntype, ttype=ntype)
            augpy_result = augpy.CudaTensor(SIZE, dtype=ctype_target)
            augpy.cast(a, augpy_result)
            augpy_result = augpy_result.numpy()
            numpy_result = safe_cast(n, ntype_target)
            augpy.default_stream.synchronize()
            @py_assert1 = augpy_result == numpy_result
            @py_assert5 = @py_assert1.all
            @py_assert7 = @py_assert5()
            if not @py_assert7:
                @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (augpy_result, numpy_result)) % {'py0':@pytest_ar._saferepr(augpy_result) if 'augpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy_result) else 'augpy_result',  'py2':@pytest_ar._saferepr(numpy_result) if 'numpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(numpy_result) else 'numpy_result'}
                @py_format9 = (@pytest_ar._format_assertmsg((ctype, ctype_target)) + '\n>assert %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.all\n}()\n}') % {'py4':@py_format3,  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert1 = @py_assert5 = @py_assert7 = None


def test_mmul_wrong_shape1():
    a = augpy.array_to_tensor(np.random.rand(200, 20).astype(np.float32))
    b = augpy.array_to_tensor(np.random.rand(20, 300).astype(np.float32))
    c = augpy.array_to_tensor(np.zeros((100, 300), np.float32))
    with pytest.raises(ValueError) as (excinfo):
        augpy.gemm(a, b, c, 1.0, 0.0)
    @py_assert0 = 'shape of C must match A*C'
    @py_assert5 = excinfo.value
    @py_assert7 = str(@py_assert5)
    @py_assert2 = @py_assert0 in @py_assert7
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.value\n})\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(excinfo) if 'excinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(excinfo) else 'excinfo',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None


def test_mmul_wrong_shape2():
    a = augpy.array_to_tensor(np.random.rand(100, 21).astype(np.float32))
    b = augpy.array_to_tensor(np.random.rand(20, 300).astype(np.float32))
    c = augpy.array_to_tensor(np.zeros((100, 300), np.float32))
    with pytest.raises(ValueError) as (excinfo):
        augpy.gemm(a, b, c, 1.0, 0.0)
    @py_assert0 = 'A.shape[1] must match B.shape[0]'
    @py_assert5 = excinfo.value
    @py_assert7 = str(@py_assert5)
    @py_assert2 = @py_assert0 in @py_assert7
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.value\n})\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(excinfo) if 'excinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(excinfo) else 'excinfo',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None


def test_add_wrong_shape1():
    for ctype, ntype in TYPES:
        result = augpy.CudaTensor((10, 10), dtype=ctype)
        a = np.arange(90, dtype=ntype).reshape((9, 10)).astype(ntype)
        b = np.arange(100, dtype=ntype).reshape((10, 10)).astype(ntype)
        c = augpy.array_to_tensor(a)
        d = augpy.array_to_tensor(b)
        with pytest.raises(ValueError) as (excinfo):
            augpy.add(c, d, result)
            augpy.tensor_to_array(result)
            augpy.default_stream.synchronize()
        @py_assert0 = 'argument 1 (dim 0=9) must broadcastable to output (dim 0=10)'
        @py_assert5 = excinfo.value
        @py_assert7 = str(@py_assert5)
        @py_assert2 = @py_assert0 in @py_assert7
        if not @py_assert2:
            @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.value\n})\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(excinfo) if 'excinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(excinfo) else 'excinfo',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None


def test_add_wrong_shape2():
    for ctype, ntype in TYPES:
        result = augpy.CudaTensor((10, 10), dtype=ctype)
        a = np.arange(100, dtype=ntype).reshape((10, 10)).astype(ntype)
        b = np.arange(90, dtype=ntype).reshape((9, 10)).astype(ntype)
        c = augpy.array_to_tensor(a)
        d = augpy.array_to_tensor(b)
        with pytest.raises(ValueError) as (excinfo):
            augpy.add(c, d, result)
            augpy.tensor_to_array(result)
            augpy.default_stream.synchronize()
        @py_assert0 = 'argument 2 (dim 0=9) must broadcastable to output (dim 0=10)'
        @py_assert5 = excinfo.value
        @py_assert7 = str(@py_assert5)
        @py_assert2 = @py_assert0 in @py_assert7
        if not @py_assert2:
            @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.value\n})\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(excinfo) if 'excinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(excinfo) else 'excinfo',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None


def test_add_wrong_shape3():
    for ctype, ntype in TYPES:
        result = augpy.CudaTensor((9, 10), dtype=ctype)
        a = np.arange(100, dtype=ntype).reshape((10, 10)).astype(ntype)
        b = np.arange(100, dtype=ntype).reshape((10, 10)).astype(ntype)
        c = augpy.array_to_tensor(a)
        d = augpy.array_to_tensor(b)
        with pytest.raises(ValueError) as (excinfo):
            augpy.add(c, d, result)
            augpy.tensor_to_array(result)
            augpy.default_stream.synchronize()
        @py_assert0 = 'argument 1 (dim 0=10) must broadcastable to output (dim 0=9)'
        @py_assert5 = excinfo.value
        @py_assert7 = str(@py_assert5)
        @py_assert2 = @py_assert0 in @py_assert7
        if not @py_assert2:
            @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.value\n})\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(excinfo) if 'excinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(excinfo) else 'excinfo',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None


def test_mul_wrong_shape1():
    for ctype, ntype in TYPES:
        result = augpy.CudaTensor((10, 10), dtype=ctype)
        a = np.arange(90, dtype=ntype).reshape((9, 10)).astype(ntype)
        b = np.arange(100, dtype=ntype).reshape((10, 10)).astype(ntype)
        c = augpy.array_to_tensor(a)
        d = augpy.array_to_tensor(b)
        with pytest.raises(ValueError) as (excinfo):
            augpy.mul(c, d, result)
            augpy.tensor_to_array(result)
            augpy.default_stream.synchronize()
        @py_assert0 = 'argument 1 (dim 0=9) must broadcastable to output (dim 0=10)'
        @py_assert5 = excinfo.value
        @py_assert7 = str(@py_assert5)
        @py_assert2 = @py_assert0 in @py_assert7
        if not @py_assert2:
            @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.value\n})\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(excinfo) if 'excinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(excinfo) else 'excinfo',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None


def test_mul_wrong_shape2():
    for ctype, ntype in TYPES:
        result = augpy.CudaTensor((10, 10), dtype=ctype)
        a = np.arange(100, dtype=ntype).reshape((10, 10)).astype(ntype)
        b = np.arange(90, dtype=ntype).reshape((9, 10)).astype(ntype)
        c = augpy.array_to_tensor(a)
        d = augpy.array_to_tensor(b)
        with pytest.raises(ValueError) as (excinfo):
            augpy.mul(c, d, result)
            augpy.tensor_to_array(result)
            augpy.default_stream.synchronize()
        @py_assert0 = 'argument 2 (dim 0=9) must broadcastable to output (dim 0=10)'
        @py_assert5 = excinfo.value
        @py_assert7 = str(@py_assert5)
        @py_assert2 = @py_assert0 in @py_assert7
        if not @py_assert2:
            @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.value\n})\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(excinfo) if 'excinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(excinfo) else 'excinfo',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None


def test_mul_wrong_shape3():
    for ctype, ntype in TYPES:
        result = augpy.CudaTensor((9, 10), dtype=ctype)
        a = np.arange(100, dtype=ntype).reshape((10, 10)).astype(ntype)
        b = np.arange(100, dtype=ntype).reshape((10, 10)).astype(ntype)
        c = augpy.array_to_tensor(a)
        d = augpy.array_to_tensor(b)
        with pytest.raises(ValueError) as (excinfo):
            augpy.mul(c, d, result)
            augpy.tensor_to_array(result)
            augpy.default_stream.synchronize()
        @py_assert0 = 'argument 1 (dim 0=10) must broadcastable to output (dim 0=9)'
        @py_assert5 = excinfo.value
        @py_assert7 = str(@py_assert5)
        @py_assert2 = @py_assert0 in @py_assert7
        if not @py_assert2:
            @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.value\n})\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(excinfo) if 'excinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(excinfo) else 'excinfo',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None


def test_div_wrong_shape1():
    for ctype, ntype in TYPES:
        result = augpy.CudaTensor((10, 10), dtype=ctype)
        a = np.arange(90, dtype=ntype).reshape((9, 10)).astype(ntype)
        b = np.arange(100, dtype=ntype).reshape((10, 10)).astype(ntype)
        c = augpy.array_to_tensor(a)
        d = augpy.array_to_tensor(b)
        with pytest.raises(ValueError) as (excinfo):
            augpy.div(c, d, result)
            augpy.tensor_to_array(result)
            augpy.default_stream.synchronize()
        @py_assert0 = 'argument 1 (dim 0=9) must broadcastable to output (dim 0=10)'
        @py_assert5 = excinfo.value
        @py_assert7 = str(@py_assert5)
        @py_assert2 = @py_assert0 in @py_assert7
        if not @py_assert2:
            @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.value\n})\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(excinfo) if 'excinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(excinfo) else 'excinfo',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None


def test_div_wrong_shape2():
    for ctype, ntype in TYPES:
        result = augpy.CudaTensor((10, 10), dtype=ctype)
        a = np.arange(100, dtype=ntype).reshape((10, 10)).astype(ntype)
        b = np.arange(90, dtype=ntype).reshape((9, 10)).astype(ntype)
        c = augpy.array_to_tensor(a)
        d = augpy.array_to_tensor(b)
        with pytest.raises(ValueError) as (excinfo):
            augpy.div(c, d, result)
            augpy.tensor_to_array(result)
            augpy.default_stream.synchronize()
        @py_assert0 = 'argument 2 (dim 0=9) must broadcastable to output (dim 0=10)'
        @py_assert5 = excinfo.value
        @py_assert7 = str(@py_assert5)
        @py_assert2 = @py_assert0 in @py_assert7
        if not @py_assert2:
            @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.value\n})\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(excinfo) if 'excinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(excinfo) else 'excinfo',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None


def test_div_wrong_shape3():
    for ctype, ntype in TYPES:
        result = augpy.CudaTensor((9, 10), dtype=ctype)
        a = np.arange(100, dtype=ntype).reshape((10, 10)).astype(ntype)
        b = np.arange(100, dtype=ntype).reshape((10, 10)).astype(ntype)
        c = augpy.array_to_tensor(a)
        d = augpy.array_to_tensor(b)
        with pytest.raises(ValueError) as (excinfo):
            augpy.div(c, d, result)
            augpy.tensor_to_array(result)
            augpy.default_stream.synchronize()
        @py_assert0 = 'argument 1 (dim 0=10) must broadcastable to output (dim 0=9)'
        @py_assert5 = excinfo.value
        @py_assert7 = str(@py_assert5)
        @py_assert2 = @py_assert0 in @py_assert7
        if not @py_assert2:
            @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.value\n})\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(excinfo) if 'excinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(excinfo) else 'excinfo',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None


def test_div_by_0_inf():
    for ctype, ntype in F_TYPES:
        result = augpy.CudaTensor((1000, ), dtype=ctype)
        a = augpy.array_to_tensor(np.arange(1000, dtype=ntype) + 1)
        b = augpy.array_to_tensor(np.asarray([0], dtype=ntype))
        augpy.div(a, b, result)
        result_array = augpy.tensor_to_array(result)
        augpy.default_stream.synchronize()
        print(result_array)
        @py_assert1 = np.isinf
        @py_assert4 = @py_assert1(result_array)
        @py_assert6 = @py_assert4.all
        @py_assert8 = @py_assert6()
        if not @py_assert8:
            @py_format10 = 'assert %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.isinf\n}(%(py3)s)\n}.all\n}()\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(result_array) if 'result_array' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result_array) else 'result_array',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None


def test_div_by_0_nan():
    for ctype, ntype in F_TYPES:
        result = augpy.CudaTensor((1000, ), dtype=ctype)
        a = augpy.array_to_tensor(np.zeros(1000, dtype=ntype))
        b = augpy.array_to_tensor(np.asarray([0], dtype=ntype))
        augpy.div(a, b, result)
        result_array = augpy.tensor_to_array(result)
        augpy.default_stream.synchronize()
        print(result_array)
        @py_assert1 = np.isnan
        @py_assert4 = @py_assert1(result_array)
        @py_assert6 = @py_assert4.all
        @py_assert8 = @py_assert6()
        if not @py_assert8:
            @py_format10 = 'assert %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.isnan\n}(%(py3)s)\n}.all\n}()\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(result_array) if 'result_array' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result_array) else 'result_array',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None


def test_sadd_wrong_shape1():
    for ctype, ntype in TYPES:
        a = np.arange(100, dtype=ntype).reshape((10, 10))
        d = augpy.CudaTensor((9, 10), dtype=ctype)
        c = augpy.array_to_tensor(a)
        rand = random.random() * 100
        with pytest.raises(ValueError) as (excinfo):
            augpy.add(c, rand, d)
            augpy.tensor_to_array(d)
            augpy.default_stream.synchronize()
        @py_assert0 = 'argument 1 (dim 0=10) must broadcastable to output (dim 0=9)'
        @py_assert5 = excinfo.value
        @py_assert7 = str(@py_assert5)
        @py_assert2 = @py_assert0 in @py_assert7
        if not @py_assert2:
            @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.value\n})\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(excinfo) if 'excinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(excinfo) else 'excinfo',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None


def test_sadd_wrong_shape2():
    for ctype, ntype in F_TYPES:
        a = np.arange(90, dtype=ntype).reshape((9, 10))
        d = augpy.CudaTensor((10, 10), dtype=ctype)
        c = augpy.array_to_tensor(a)
        rand = random.random() * 100
        with pytest.raises(ValueError) as (excinfo):
            augpy.add(c, rand, d)
            augpy.tensor_to_array(d)
            augpy.default_stream.synchronize()
        @py_assert0 = 'argument 1 (dim 0=9) must broadcastable to output (dim 0=10)'
        @py_assert5 = excinfo.value
        @py_assert7 = str(@py_assert5)
        @py_assert2 = @py_assert0 in @py_assert7
        if not @py_assert2:
            @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.value\n})\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(excinfo) if 'excinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(excinfo) else 'excinfo',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None


def test_add_scalar1():
    __random((augpy.add), (lambda a, b: a + b), size1=SIZE, size2=(1, ))


if __name__ == '__main__':
    test_add_scalar1()

def test_add_scalar2():
    __random((augpy.add), (lambda a, b: a + b), size1=(1, ), size2=SIZE)


def test_add_scalar_scalar():
    __random((augpy.add), (lambda a, b: a + b), size1=(1, ), size2=(1, ))


def test_add_scalar_as_target():
    __random((augpy.add), (lambda a, b: a + b), size1=(), size2=(), size3=())


def test_sub_scalar1():
    __random((augpy.sub), (lambda a, b: a - b), size1=SIZE, size2=(1, ))


def test_sub_scalar2():
    __random((augpy.sub), (lambda a, b: a - b), size1=(1, ), size2=SIZE)


def test_sub_scalar_scalar():
    __random((augpy.sub), (lambda a, b: a - b), size1=(1, ), size2=(1, ))


def test_sub_scalar_as_target():
    __random((augpy.sub), (lambda a, b: a - b), size1=(), size2=(), size3=())


def test_mul_scalar1():
    __random((augpy.mul), (lambda a, b: a * b), size1=SIZE, size2=(1, ))


def test_mul_scalar2():
    __random((augpy.mul), (lambda a, b: a * b), size1=(1, ), size2=SIZE)


def test_mul_scalar_scalar():
    __random((augpy.mul), (lambda a, b: a * b), size1=(1, ), size2=(1, ))


def test_mul_scalar_as_target():
    __random((augpy.mul), (lambda a, b: a * b), size1=(), size2=(), size3=())


def test_div_scalar1():
    __random((augpy.div), (lambda a, b: a / b), size1=SIZE, size2=(1, ), close_allowed=True)


def test_div_scalar2():
    __random((augpy.div), (lambda a, b: a / b), size1=(1, ), size2=SIZE, close_allowed=True)


def test_div_scalar_scalar():
    __random((augpy.div), (lambda a, b: a / b), size1=(1, ), size2=(1, ), close_allowed=True)


def test_div_scalar_as_target():
    __random((augpy.div), (lambda a, b: a / b), size1=(), size2=(), size3=(), close_allowed=True)


def test_sum():
    __random_unary((lambda a: a.sum(upcast=False)), (lambda a: a.sum(dtype=(a.dtype))), size=SIZE,
      close_allowed=True,
      cast=True)


def test_sum_upcast():
    __random_unary((lambda a: a.sum(upcast=True)), (lambda a: a.sum(dtype=(a.dtype))), size=SIZE,
      close_allowed=True,
      cast=False)


def test_sum_axis():
    __random_unary((lambda a: a.sum(1, upcast=False)), (lambda a: a.sum(axis=1, dtype=(a.dtype))), size=SIZE,
      close_allowed=True,
      cast=True)


def test_sum_axis_upcast():
    __random_unary((lambda a: a.sum(1, upcast=True)), (lambda a: a.sum(axis=1, dtype=(a.dtype))), size=SIZE,
      close_allowed=True,
      cast=False)