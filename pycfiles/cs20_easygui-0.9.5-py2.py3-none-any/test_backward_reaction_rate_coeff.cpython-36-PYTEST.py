# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/benjaminrafetto/Code/cs207/cs207-FinalProject/build/lib/kinetics/test/test_backward_reaction_rate_coeff.py
# Compiled at: 2017-12-08 16:35:10
# Size of source mod 2**32: 3051 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from kinetics import chemkin
import numpy as np
reactions = chemkin.Reaction((chemkin.ReactionParser('kinetics/test/xml/xml_homework.xml')), T=3500)

class test_Backward_Reaction_Coeffs(unittest.TestCase):

    def test_H_over_RT_result(self):
        H_O2 = np.array([[2.50000001, -2.30842973e-11, 1.61561948e-14, -4.73515235e-18, 4.98197357e-22, 25473.6599, -0.44668291], [3.28253784, 0.00148308754, -7.57966669e-07, 2.09470555e-10, -2.16717794e-14, -1088.45772, 5.4532312]]).T
        Tmax = 3500.0
        compare = np.array([3.69508857, 4.06676078, 5.08138715, 6.28213553, -2.93437561])
        reactions.get_nasa_coeffs = H_O2
        output = reactions.H_over_RT()
        @py_assert1 = np.equal
        @py_assert5 = @py_assert1(output, compare)
        @py_assert7 = @py_assert5.all
        @py_assert9 = @py_assert7()
        @py_assert12 = 0
        @py_assert11 = @py_assert9 == @py_assert12
        if not @py_assert11:
            @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.equal\n}(%(py3)s, %(py4)s)\n}.all\n}()\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py4':@pytest_ar._saferepr(compare) if 'compare' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compare) else 'compare',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
            @py_format16 = (@pytest_ar._format_assertmsg('Expected outcome') + '\n>assert %(py15)s') % {'py15': @py_format14}
            raise AssertionError(@pytest_ar._format_explanation(@py_format16))
        @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None

    def test_H_over_RT_bad_result(self):
        H_O2 = np.array([[2.50000001, -2.30842973e-11, 1.61561948e-14, -4.73515235e-18, 4.98197357e-22, 25473.6599, -0.44668291], [3.28253784, 0.00148308754, -7.57966669e-07, 2.09470555e-10, -2.16717794e-14, -1088.45772, 5.4532312]]).T
        Tmax = 3500.0
        compare = np.array([3.59508857, 4.26676078, 5.98138715, 6.48213553, -2.73437561])
        reactions.get_nasa_coeffs = H_O2
        output = reactions.H_over_RT()
        @py_assert1 = np.equal
        @py_assert5 = @py_assert1(output, compare)
        @py_assert7 = @py_assert5.any
        @py_assert9 = @py_assert7()
        @py_assert12 = False
        @py_assert11 = @py_assert9 == @py_assert12
        if not @py_assert11:
            @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.equal\n}(%(py3)s, %(py4)s)\n}.any\n}()\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py4':@pytest_ar._saferepr(compare) if 'compare' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compare) else 'compare',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
            @py_format16 = (@pytest_ar._format_assertmsg('Unexpected outcome') + '\n>assert %(py15)s') % {'py15': @py_format14}
            raise AssertionError(@pytest_ar._format_explanation(@py_format16))
        @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None

    def test_reaction_H_over_RT_argument_number(self):
        try:
            chemkin.Reaction.H_over_RT(10000, 100, 10000000)
        except TypeError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == TypeError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, TypeError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(TypeError) if 'TypeError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TypeError) else 'TypeError'}
                @py_format8 = (@pytest_ar._format_assertmsg('Wrong args number') + '\n>assert %(py7)s') % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_S_over_R_result(self):
        H_O2 = np.array([[2.50000001, -2.30842973e-11, 1.61561948e-14, -4.73515235e-18, 4.98197357e-22, 25473.6599, -0.44668291], [3.28253784, 0.00148308754, -7.57966669e-07, 2.09470555e-10, -2.16717794e-14, -1088.45772, 5.4532312]]).T
        Tmax = 3500.0
        compare = np.array([3.69508857, 4.06676078, 5.08138715, 6.28213553, -2.93437561])
        reactions.get_nasa_coeffs = H_O2
        output = reactions.S_over_R()
        @py_assert1 = np.equal
        @py_assert5 = @py_assert1(output, compare)
        @py_assert7 = @py_assert5.all
        @py_assert9 = @py_assert7()
        @py_assert12 = 0
        @py_assert11 = @py_assert9 == @py_assert12
        if not @py_assert11:
            @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.equal\n}(%(py3)s, %(py4)s)\n}.all\n}()\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py4':@pytest_ar._saferepr(compare) if 'compare' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compare) else 'compare',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
            @py_format16 = (@pytest_ar._format_assertmsg('Expected outcome') + '\n>assert %(py15)s') % {'py15': @py_format14}
            raise AssertionError(@pytest_ar._format_explanation(@py_format16))
        @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None

    def test_S_over_R_bad_result(self):
        H_O2 = np.array([[2.50000001, -2.30842973e-11, 1.61561948e-14, -4.73515235e-18, 4.98197357e-22, 25473.6599, -0.44668291], [3.28253784, 0.00148308754, -7.57966669e-07, 2.09470555e-10, -2.16717794e-14, -1088.45772, 5.4532312]]).T
        Tmax = 3500.0
        compare = np.array([3.59508857, 4.26676078, 5.98138715, 6.48213553, -2.73437561])
        reactions.get_nasa_coeffs = H_O2
        output = reactions.S_over_R()
        @py_assert1 = np.equal
        @py_assert5 = @py_assert1(output, compare)
        @py_assert7 = @py_assert5.any
        @py_assert9 = @py_assert7()
        @py_assert12 = False
        @py_assert11 = @py_assert9 == @py_assert12
        if not @py_assert11:
            @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.equal\n}(%(py3)s, %(py4)s)\n}.any\n}()\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py4':@pytest_ar._saferepr(compare) if 'compare' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compare) else 'compare',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
            @py_format16 = (@pytest_ar._format_assertmsg('Unexpected outcome') + '\n>assert %(py15)s') % {'py15': @py_format14}
            raise AssertionError(@pytest_ar._format_explanation(@py_format16))
        @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None

    def test_reaction_S_over_R_argument_number(self):
        try:
            chemkin.Reaction.S_over_R(10000, 100, 10000000)
        except TypeError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == TypeError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, TypeError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(TypeError) if 'TypeError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TypeError) else 'TypeError'}
                @py_format8 = (@pytest_ar._format_assertmsg('Wrong args number') + '\n>assert %(py7)s') % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None