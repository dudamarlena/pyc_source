# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/folz/DFKI/Hacks/augpy/test/test_rng.py
# Compiled at: 2020-01-24 11:34:18
# Size of source mod 2**32: 1538 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, sys
sys.path.append(os.pardir)
from math import sqrt
import numpy as np, augpy
N, C, H, W = (16, 3, 128, 128)
I_TYPES = [
 (
  augpy.uint8, np.uint8),
 (
  augpy.int8, np.int8),
 (
  augpy.int16, np.int16),
 (
  augpy.uint16, np.uint16),
 (
  augpy.int32, np.int32),
 (
  augpy.uint32, np.uint32),
 (
  augpy.int64, np.int64),
 (
  augpy.uint64, np.uint64)]
F_TYPES = [
 (
  augpy.float32, np.float32),
 (
  augpy.float64, np.float64)]
TYPES = I_TYPES + F_TYPES
gen = augpy.RandomNumberGenerator(seed=1337)

def test_uniform():
    for ctype, ntype in TYPES:
        noise = augpy.CudaTensor((1000000, ), dtype=ctype)
        minv = 5
        maxv = 123
        gen.uniform(noise, minv, maxv)
        array = noise.numpy()
        augpy.default_stream.synchronize()
        true_mean = (maxv + minv) / 2
        @py_assert2 = array.mean
        @py_assert4 = @py_assert2()
        @py_assert7 = @py_assert4 - true_mean
        @py_assert8 = abs(@py_assert7)
        @py_assert11 = 0.3
        @py_assert10 = @py_assert8 < @py_assert11
        if not @py_assert10:
            @py_format13 = @pytest_ar._call_reprcompare(('<', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s((%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.mean\n}()\n} - %(py6)s))\n} < %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(abs) if 'abs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(abs) else 'abs',  'py1':@pytest_ar._saferepr(array) if 'array' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(array) else 'array',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(true_mean) if 'true_mean' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(true_mean) else 'true_mean',  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
            @py_format15 = (@pytest_ar._format_assertmsg((ctype, 'incorrect mean')) + '\n>assert %(py14)s') % {'py14': @py_format13}
            raise AssertionError(@pytest_ar._format_explanation(@py_format15))
        @py_assert2 = @py_assert4 = @py_assert7 = @py_assert8 = @py_assert10 = @py_assert11 = None
        @py_assert1 = array.min
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3 >= minv
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.min\n}()\n} >= %(py6)s', ), (@py_assert3, minv)) % {'py0':@pytest_ar._saferepr(array) if 'array' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(array) else 'array',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(minv) if 'minv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(minv) else 'minv'}
            @py_format9 = (@pytest_ar._format_assertmsg((ctype, 'incorrect min value')) + '\n>assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = array.max
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3 <= maxv
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('<=', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.max\n}()\n} <= %(py6)s', ), (@py_assert3, maxv)) % {'py0':@pytest_ar._saferepr(array) if 'array' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(array) else 'array',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(maxv) if 'maxv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(maxv) else 'maxv'}
            @py_format9 = (@pytest_ar._format_assertmsg((ctype, 'incorrect max value')) + '\n>assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None


def test_gaussian():
    for ctype, ntype in TYPES:
        noise = augpy.CudaTensor((10000000, ), dtype=ctype)
        gen.gaussian(noise, 64, 7)
        array = noise.numpy()
        augpy.default_stream.synchronize()
        @py_assert2 = array.mean
        @py_assert4 = @py_assert2()
        @py_assert6 = 64
        @py_assert8 = @py_assert4 - @py_assert6
        @py_assert9 = abs(@py_assert8)
        @py_assert12 = 0.05
        @py_assert11 = @py_assert9 < @py_assert12
        if not @py_assert11:
            @py_format14 = @pytest_ar._call_reprcompare(('<', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s((%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.mean\n}()\n} - %(py7)s))\n} < %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(abs) if 'abs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(abs) else 'abs',  'py1':@pytest_ar._saferepr(array) if 'array' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(array) else 'array',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
            @py_format16 = (@pytest_ar._format_assertmsg((ctype, 'incorrect mean')) + '\n>assert %(py15)s') % {'py15': @py_format14}
            raise AssertionError(@pytest_ar._format_explanation(@py_format16))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert12 = None
        @py_assert2 = array.std
        @py_assert4 = @py_assert2()
        @py_assert6 = 7
        @py_assert8 = @py_assert4 - @py_assert6
        @py_assert9 = abs(@py_assert8)
        @py_assert12 = 0.05
        @py_assert11 = @py_assert9 < @py_assert12
        if not @py_assert11:
            @py_format14 = @pytest_ar._call_reprcompare(('<', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s((%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.std\n}()\n} - %(py7)s))\n} < %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(abs) if 'abs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(abs) else 'abs',  'py1':@pytest_ar._saferepr(array) if 'array' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(array) else 'array',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
            @py_format16 = (@pytest_ar._format_assertmsg((ctype, 'incorrect standard deviation')) + '\n>assert %(py15)s') % {'py15': @py_format14}
            raise AssertionError(@pytest_ar._format_explanation(@py_format16))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert12 = None