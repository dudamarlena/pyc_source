# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/david/gits/pyGaussDCA/tests/test_gaussdca.py
# Compiled at: 2019-06-25 04:41:24
# Size of source mod 2**32: 2078 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, gaussdca
base_path = os.path.dirname(__file__)

def test_weights_small_auto():
    w = gaussdca.compute_weights(os.path.join(base_path, 'data/small.a3m'))
    @py_assert1 = w.shape
    @py_assert4 = (13279, )
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=9)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.shape\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = w.max
    @py_assert3 = @py_assert1()
    @py_assert6 = 1.0
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=10)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.max\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = w.min
    @py_assert4 = @py_assert2()
    @py_assert6 = 0.0014619883040935672
    @py_assert8 = @py_assert4 - @py_assert6
    @py_assert9 = abs(@py_assert8)
    @py_assert12 = 1e-09
    @py_assert11 = @py_assert9 < @py_assert12
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=11)
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('<', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s((%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.min\n}()\n} - %(py7)s))\n} < %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(abs) if 'abs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(abs) else 'abs',  'py1':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert2 = w.mean
    @py_assert4 = @py_assert2()
    @py_assert6 = 0.1802026091608966
    @py_assert8 = @py_assert4 - @py_assert6
    @py_assert9 = abs(@py_assert8)
    @py_assert12 = 2e-05
    @py_assert11 = @py_assert9 < @py_assert12
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=12)
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('<', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s((%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.mean\n}()\n} - %(py7)s))\n} < %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(abs) if 'abs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(abs) else 'abs',  'py1':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert12 = None


def test_all_small_auto():
    result = gaussdca.run(os.path.join(base_path, 'data/small.a3m'))
    N = 53
    @py_assert0 = result['gdca']
    @py_assert2 = @py_assert0.shape
    @py_assert5 = (
     N, N)
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=20)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.shape\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = result['gdca_corr']
    @py_assert2 = @py_assert0.shape
    @py_assert5 = (
     N, N)
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=21)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.shape\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = result['gdca']
    @py_assert2 = @py_assert0.diagonal
    @py_assert4 = @py_assert2()
    @py_assert6 = @py_assert4.sum
    @py_assert8 = @py_assert6()
    @py_assert11 = 0.0
    @py_assert10 = @py_assert8 == @py_assert11
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=24)
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.diagonal\n}()\n}.sum\n}()\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    @py_assert0 = result['gdca_corr']
    @py_assert2 = @py_assert0.diagonal
    @py_assert4 = @py_assert2()
    @py_assert6 = @py_assert4.sum
    @py_assert8 = @py_assert6()
    @py_assert11 = 0.0
    @py_assert10 = @py_assert8 == @py_assert11
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=25)
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.diagonal\n}()\n}.sum\n}()\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    sym = result['gdca'] - result['gdca'].T
    @py_assert1 = sym.max
    @py_assert3 = @py_assert1()
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=29)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.max\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(sym) if 'sym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sym) else 'sym',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = sym.min
    @py_assert3 = @py_assert1()
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=30)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.min\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(sym) if 'sym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sym) else 'sym',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    sym = result['gdca_corr'] - result['gdca_corr'].T
    @py_assert1 = sym.max
    @py_assert3 = @py_assert1()
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=32)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.max\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(sym) if 'sym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sym) else 'sym',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = sym.min
    @py_assert3 = @py_assert1()
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=33)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.min\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(sym) if 'sym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sym) else 'sym',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert0 = result['seq']
    @py_assert3 = 13279
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=36)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = result['eff_seq']
    @py_assert3 = 2392.921
    @py_assert5 = @py_assert1 - @py_assert3
    @py_assert6 = abs(@py_assert5)
    @py_assert9 = 0.1
    @py_assert8 = @py_assert6 < @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=37)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('<', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s((%(py2)s - %(py4)s))\n} < %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(abs) if 'abs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(abs) else 'abs',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_weights_small_fixed_theta():
    w = gaussdca.compute_weights(os.path.join(base_path, 'data/small.a3m'), 0.3)
    @py_assert1 = w.shape
    @py_assert4 = (13279, )
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=42)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.shape\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = w.max
    @py_assert3 = @py_assert1()
    @py_assert6 = 1.0
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=43)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.max\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = w.min
    @py_assert4 = @py_assert2()
    @py_assert6 = 0.0014727540500736377
    @py_assert8 = @py_assert4 - @py_assert6
    @py_assert9 = abs(@py_assert8)
    @py_assert12 = 1e-09
    @py_assert11 = @py_assert9 < @py_assert12
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=44)
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('<', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s((%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.min\n}()\n} - %(py7)s))\n} < %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(abs) if 'abs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(abs) else 'abs',  'py1':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert12 = None
    @py_assert2 = w.mean
    @py_assert4 = @py_assert2()
    @py_assert6 = 0.295421949941903
    @py_assert8 = @py_assert4 - @py_assert6
    @py_assert9 = abs(@py_assert8)
    @py_assert12 = 2e-05
    @py_assert11 = @py_assert9 < @py_assert12
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=45)
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('<', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py0)s((%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.mean\n}()\n} - %(py7)s))\n} < %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(abs) if 'abs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(abs) else 'abs',  'py1':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert11 = @py_assert12 = None


def test_weights_large_auto():
    w = gaussdca.compute_weights(os.path.join(base_path, 'data/large.a3m'))
    @py_assert1 = w.shape
    @py_assert4 = (35555, )
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=50)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.shape\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_weights_large_fixed_theta():
    w = gaussdca.compute_weights(os.path.join(base_path, 'data/large.a3m'), 0.3)
    @py_assert1 = w.shape
    @py_assert4 = (35555, )
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=56)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.shape\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(w) if 'w' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(w) else 'w',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_all_large_auto():
    result = gaussdca.run(os.path.join(base_path, 'data/large.a3m'))
    N = 465
    @py_assert0 = result['gdca']
    @py_assert2 = @py_assert0.shape
    @py_assert5 = (
     N, N)
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=65)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.shape\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = result['gdca_corr']
    @py_assert2 = @py_assert0.shape
    @py_assert5 = (
     N, N)
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=66)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.shape\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = result['gdca']
    @py_assert2 = @py_assert0.diagonal
    @py_assert4 = @py_assert2()
    @py_assert6 = @py_assert4.sum
    @py_assert8 = @py_assert6()
    @py_assert11 = 0.0
    @py_assert10 = @py_assert8 == @py_assert11
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=69)
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.diagonal\n}()\n}.sum\n}()\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    @py_assert0 = result['gdca_corr']
    @py_assert2 = @py_assert0.diagonal
    @py_assert4 = @py_assert2()
    @py_assert6 = @py_assert4.sum
    @py_assert8 = @py_assert6()
    @py_assert11 = 0.0
    @py_assert10 = @py_assert8 == @py_assert11
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=70)
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.diagonal\n}()\n}.sum\n}()\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    @py_assert0 = result['seq']
    @py_assert3 = 35555
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/david/gits/pyGaussDCA/tests/test_gaussdca.py', lineno=73)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None