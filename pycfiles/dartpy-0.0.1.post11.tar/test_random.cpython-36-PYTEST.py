# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/js/dev/prl/dart/pybind11/python/tests/unit/math/test_random.py
# Compiled at: 2019-01-11 23:38:31
# Size of source mod 2**32: 790 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, platform, pytest
from dartpy.math import Random

def test_create():
    rand = Random()


def test_seed():
    rand = Random()
    N = 10
    min = -10
    max = 10
    first = []
    second = []
    third = []
    tol = 1e-06
    for i in range(N):
        Random.setSeed(i)
        first.append(Random.uniform(min, max))
        second.append(Random.uniform(min, max))
        third.append(Random.uniform(min, max))

    for i in range(N):
        Random.setSeed(i)
        @py_assert1 = Random.getSeed
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3 is i
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('is',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.getSeed\n}()\n} is %(py6)s',), (@py_assert3, i)) % {'py0':@pytest_ar._saferepr(Random) if 'Random' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Random) else 'Random',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i'}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = Random.uniform
        @py_assert5 = @py_assert1(min, max)
        @py_assert9 = pytest.approx
        @py_assert11 = first[i]
        @py_assert14 = @py_assert9(@py_assert11, tol)
        @py_assert7 = @py_assert5 == @py_assert14
        if not @py_assert7:
            @py_format16 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.uniform\n}(%(py3)s, %(py4)s)\n} == %(py15)s\n{%(py15)s = %(py10)s\n{%(py10)s = %(py8)s.approx\n}(%(py12)s, %(py13)s)\n}',), (@py_assert5, @py_assert14)) % {'py0':@pytest_ar._saferepr(Random) if 'Random' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Random) else 'Random',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(min) if 'min' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(min) else 'min',  'py4':@pytest_ar._saferepr(max) if 'max' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(max) else 'max',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(pytest) if 'pytest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pytest) else 'pytest',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py13':@pytest_ar._saferepr(tol) if 'tol' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tol) else 'tol',  'py15':@pytest_ar._saferepr(@py_assert14)}
            @py_format18 = ('' + 'assert %(py17)s') % {'py17': @py_format16}
            raise AssertionError(@pytest_ar._format_explanation(@py_format18))
        @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert14 = None
        @py_assert1 = Random.uniform
        @py_assert5 = @py_assert1(min, max)
        @py_assert9 = pytest.approx
        @py_assert11 = second[i]
        @py_assert14 = @py_assert9(@py_assert11, tol)
        @py_assert7 = @py_assert5 == @py_assert14
        if not @py_assert7:
            @py_format16 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.uniform\n}(%(py3)s, %(py4)s)\n} == %(py15)s\n{%(py15)s = %(py10)s\n{%(py10)s = %(py8)s.approx\n}(%(py12)s, %(py13)s)\n}',), (@py_assert5, @py_assert14)) % {'py0':@pytest_ar._saferepr(Random) if 'Random' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Random) else 'Random',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(min) if 'min' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(min) else 'min',  'py4':@pytest_ar._saferepr(max) if 'max' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(max) else 'max',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(pytest) if 'pytest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pytest) else 'pytest',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py13':@pytest_ar._saferepr(tol) if 'tol' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tol) else 'tol',  'py15':@pytest_ar._saferepr(@py_assert14)}
            @py_format18 = ('' + 'assert %(py17)s') % {'py17': @py_format16}
            raise AssertionError(@pytest_ar._format_explanation(@py_format18))
        @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert14 = None
        @py_assert1 = Random.uniform
        @py_assert5 = @py_assert1(min, max)
        @py_assert9 = pytest.approx
        @py_assert11 = third[i]
        @py_assert14 = @py_assert9(@py_assert11, tol)
        @py_assert7 = @py_assert5 == @py_assert14
        if not @py_assert7:
            @py_format16 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.uniform\n}(%(py3)s, %(py4)s)\n} == %(py15)s\n{%(py15)s = %(py10)s\n{%(py10)s = %(py8)s.approx\n}(%(py12)s, %(py13)s)\n}',), (@py_assert5, @py_assert14)) % {'py0':@pytest_ar._saferepr(Random) if 'Random' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Random) else 'Random',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(min) if 'min' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(min) else 'min',  'py4':@pytest_ar._saferepr(max) if 'max' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(max) else 'max',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(pytest) if 'pytest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pytest) else 'pytest',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py13':@pytest_ar._saferepr(tol) if 'tol' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tol) else 'tol',  'py15':@pytest_ar._saferepr(@py_assert14)}
            @py_format18 = ('' + 'assert %(py17)s') % {'py17': @py_format16}
            raise AssertionError(@pytest_ar._format_explanation(@py_format18))
        @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert14 = None


if __name__ == '__main__':
    pytest.main()