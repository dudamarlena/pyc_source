# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benjaminrafetto/Code/cs207/cs207-FinalProject/build/lib/kinetics/test/test_reaction.py
# Compiled at: 2017-12-08 16:35:00
# Size of source mod 2**32: 1312 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sys, numpy as np, unittest
from kinetics import chemkin

class test_reactions(unittest.TestCase):

    def test_reaction_result(self):
        V1, V2 = np.array([[1, 2, 3], [2, 1, 2]]).T, np.array([[1, 1, 2], [5, 1, 1]]).T
        X = [1, 2, 1]
        k = [6, 6]
        compare = np.array([36, -24, -36])
        output = chemkin.ChemKin.reaction_rate(V1, V2, X, k)
        @py_assert1 = np.equal
        @py_assert5 = @py_assert1(output, compare)
        @py_assert7 = @py_assert5.all
        @py_assert9 = @py_assert7()
        @py_assert12 = 1
        @py_assert11 = @py_assert9 == @py_assert12
        if not @py_assert11:
            @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.equal\n}(%(py3)s, %(py4)s)\n}.all\n}()\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py4':@pytest_ar._saferepr(compare) if 'compare' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compare) else 'compare',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
            @py_format16 = (@pytest_ar._format_assertmsg('Unexpected outcome') + '\n>assert %(py15)s') % {'py15': @py_format14}
            raise AssertionError(@pytest_ar._format_explanation(@py_format16))
        @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None

    def test_reaction_type_error(self):
        V1, V2 = np.array([[1, 2, 'lol'], [2, 1, 2]]).T, np.array([[1, 'test', 2], [5, 1, 1]]).T
        X = [1, 2, 1]
        k = [6, 6]
        try:
            chemkin.ChemKin.reaction_rate(V1, V2, X, k)
        except Exception as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == TypeError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, TypeError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(TypeError) if 'TypeError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TypeError) else 'TypeError'}
                @py_format8 = (@pytest_ar._format_assertmsg('Bad args format') + '\n>assert %(py7)s') % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_reaction_coeff_pos(self):
        V1, V2 = np.array([[1, 2, 3], [2, 1, 2]]).T, np.array([[1, 1, 2], [5, 1, 1]]).T
        X = [1, 2, 1]
        k = [6, -6]
        try:
            chemkin.ChemKin.reaction_rate(V1, V2, X, k)
        except Exception as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = (@pytest_ar._format_assertmsg('Bad k') + '\n>assert %(py7)s') % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None