# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benjaminrafetto/Code/cs207/cs207-FinalProject/build/lib/kinetics/test/test_reaction_coeff.py
# Compiled at: 2017-12-11 01:33:06
# Size of source mod 2**32: 6136 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from kinetics import chemkin

class test_reaction_coeffs(unittest.TestCase):

    def test_constant_value(self):
        @py_assert1 = chemkin.ChemKin
        @py_assert3 = @py_assert1.reaction_coeff
        @py_assert5 = @py_assert3.constant
        @py_assert7 = 10
        @py_assert9 = 4
        @py_assert11 = @py_assert7 ** @py_assert9
        @py_assert12 = @py_assert5(@py_assert11)
        @py_assert15 = 10
        @py_assert17 = 4
        @py_assert19 = @py_assert15 ** @py_assert17
        @py_assert14 = @py_assert12 == @py_assert19
        if not @py_assert14:
            @py_format20 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.ChemKin\n}.reaction_coeff\n}.constant\n}((%(py8)s ** %(py10)s))\n} == (%(py16)s ** %(py18)s)', ), (@py_assert12, @py_assert19)) % {'py0':@pytest_ar._saferepr(chemkin) if 'chemkin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chemkin) else 'chemkin',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
            @py_format22 = 'assert %(py21)s' % {'py21': @py_format20}
            raise AssertionError(@pytest_ar._format_explanation(@py_format22))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = @py_assert14 = @py_assert15 = @py_assert17 = @py_assert19 = None

    def test_constant_value_decimals(self):
        @py_assert1 = chemkin.ChemKin
        @py_assert3 = @py_assert1.reaction_coeff
        @py_assert5 = @py_assert3.constant
        @py_assert7 = 4.734
        @py_assert9 = @py_assert5(@py_assert7)
        @py_assert12 = 4.734
        @py_assert11 = @py_assert9 == @py_assert12
        if not @py_assert11:
            @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.ChemKin\n}.reaction_coeff\n}.constant\n}(%(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(chemkin) if 'chemkin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chemkin) else 'chemkin',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
            @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
            raise AssertionError(@pytest_ar._format_explanation(@py_format16))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None

    def test_Arrhenius_value(self):
        @py_assert1 = chemkin.ChemKin
        @py_assert3 = @py_assert1.reaction_coeff
        @py_assert5 = @py_assert3.arr
        @py_assert7 = 10
        @py_assert9 = 2
        @py_assert11 = @py_assert7 ** @py_assert9
        @py_assert12 = 10
        @py_assert14 = 7
        @py_assert16 = @py_assert12 ** @py_assert14
        @py_assert17 = 10
        @py_assert19 = 3
        @py_assert21 = @py_assert17 ** @py_assert19
        @py_assert22 = @py_assert5(@py_assert11, A=@py_assert16, E=@py_assert21)
        @py_assert25 = 3003549.088963961
        @py_assert24 = @py_assert22 == @py_assert25
        if not @py_assert24:
            @py_format27 = @pytest_ar._call_reprcompare(('==', ), (@py_assert24,), ('%(py23)s\n{%(py23)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.ChemKin\n}.reaction_coeff\n}.arr\n}((%(py8)s ** %(py10)s), A=(%(py13)s ** %(py15)s), E=(%(py18)s ** %(py20)s))\n} == %(py26)s', ), (@py_assert22, @py_assert25)) % {'py0':@pytest_ar._saferepr(chemkin) if 'chemkin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chemkin) else 'chemkin',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py23':@pytest_ar._saferepr(@py_assert22),  'py26':@pytest_ar._saferepr(@py_assert25)}
            @py_format29 = 'assert %(py28)s' % {'py28': @py_format27}
            raise AssertionError(@pytest_ar._format_explanation(@py_format29))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert22 = @py_assert24 = @py_assert25 = None

    def test_Arrhenius_value_double_check(self):
        @py_assert1 = chemkin.ChemKin
        @py_assert3 = @py_assert1.reaction_coeff
        @py_assert5 = @py_assert3.arr
        @py_assert7 = 10
        @py_assert9 = 4
        @py_assert11 = @py_assert7 ** @py_assert9
        @py_assert12 = 10
        @py_assert14 = 3
        @py_assert16 = @py_assert12 ** @py_assert14
        @py_assert17 = 10
        @py_assert19 = 4
        @py_assert21 = @py_assert17 ** @py_assert19
        @py_assert22 = @py_assert5(@py_assert11, A=@py_assert16, E=@py_assert21)
        @py_assert25 = 886.6729784121057
        @py_assert24 = @py_assert22 == @py_assert25
        if not @py_assert24:
            @py_format27 = @pytest_ar._call_reprcompare(('==', ), (@py_assert24,), ('%(py23)s\n{%(py23)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.ChemKin\n}.reaction_coeff\n}.arr\n}((%(py8)s ** %(py10)s), A=(%(py13)s ** %(py15)s), E=(%(py18)s ** %(py20)s))\n} == %(py26)s', ), (@py_assert22, @py_assert25)) % {'py0':@pytest_ar._saferepr(chemkin) if 'chemkin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chemkin) else 'chemkin',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py23':@pytest_ar._saferepr(@py_assert22),  'py26':@pytest_ar._saferepr(@py_assert25)}
            @py_format29 = 'assert %(py28)s' % {'py28': @py_format27}
            raise AssertionError(@pytest_ar._format_explanation(@py_format29))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert22 = @py_assert24 = @py_assert25 = None

    def test_Arrhenius_argument_number(self):
        try:
            chemkin.ChemKin.reaction_coeff.arr(10000, 100, A=10000000, E=1000)
        except TypeError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == TypeError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, TypeError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(TypeError) if 'TypeError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TypeError) else 'TypeError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_type_A(self):
        try:
            chemkin.ChemKin.reaction_coeff.arr(100, A='panama', E=1000)
        except TypeError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == TypeError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, TypeError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(TypeError) if 'TypeError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TypeError) else 'TypeError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_type_E(self):
        try:
            chemkin.ChemKin.reaction_coeff.arr(1000, A=10000000, E='panama')
        except TypeError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == TypeError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, TypeError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(TypeError) if 'TypeError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TypeError) else 'TypeError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_type_T(self):
        try:
            chemkin.ChemKin.reaction_coeff.arr('panama', A=10000000, E=1000)
        except TypeError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == TypeError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, TypeError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(TypeError) if 'TypeError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TypeError) else 'TypeError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_value_negative_A(self):
        try:
            chemkin.ChemKin.reaction_coeff.arr(100, A=(-10000000), E=1000)
        except ValueError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_value_negative_E(self):
        try:
            chemkin.ChemKin.reaction_coeff.arr(100, A=10000000, E=(-1000))
        except ValueError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_value_negative_T(self):
        try:
            chemkin.ChemKin.reaction_coeff.arr((-100), A=10000000, E=1000)
        except ValueError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_flow_A(self):
        try:
            chemkin.ChemKin.reaction_coeff.arr(100, A=(float('inf')), E=1000)
        except ValueError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_flow_E(self):
        try:
            chemkin.ChemKin.reaction_coeff.arr(100, A=1000, E=(float('inf')))
        except ValueError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_flow_T(self):
        try:
            chemkin.ChemKin.reaction_coeff.arr((float('inf')), A=100, E=1000)
        except ValueError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_modified_value(self):
        @py_assert1 = chemkin.ChemKin
        @py_assert3 = @py_assert1.reaction_coeff
        @py_assert5 = @py_assert3.mod_arr
        @py_assert7 = 10
        @py_assert9 = 2
        @py_assert11 = @py_assert7 ** @py_assert9
        @py_assert12 = 10
        @py_assert14 = 7
        @py_assert16 = @py_assert12 ** @py_assert14
        @py_assert17 = 0.5
        @py_assert19 = 10
        @py_assert21 = 3
        @py_assert23 = @py_assert19 ** @py_assert21
        @py_assert24 = @py_assert5(@py_assert11, A=@py_assert16, b=@py_assert17, E=@py_assert23)
        @py_assert27 = 30035490.88963961
        @py_assert26 = @py_assert24 == @py_assert27
        if not @py_assert26:
            @py_format29 = @pytest_ar._call_reprcompare(('==', ), (@py_assert26,), ('%(py25)s\n{%(py25)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.ChemKin\n}.reaction_coeff\n}.mod_arr\n}((%(py8)s ** %(py10)s), A=(%(py13)s ** %(py15)s), b=%(py18)s, E=(%(py20)s ** %(py22)s))\n} == %(py28)s', ), (@py_assert24, @py_assert27)) % {'py0':@pytest_ar._saferepr(chemkin) if 'chemkin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chemkin) else 'chemkin',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py22':@pytest_ar._saferepr(@py_assert21),  'py25':@pytest_ar._saferepr(@py_assert24),  'py28':@pytest_ar._saferepr(@py_assert27)}
            @py_format31 = 'assert %(py30)s' % {'py30': @py_format29}
            raise AssertionError(@pytest_ar._format_explanation(@py_format31))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert24 = @py_assert26 = @py_assert27 = None

    def test_Arrhenius_modified_value_double_check(self):
        @py_assert1 = chemkin.ChemKin
        @py_assert3 = @py_assert1.reaction_coeff
        @py_assert5 = @py_assert3.mod_arr
        @py_assert7 = 10
        @py_assert9 = 2
        @py_assert11 = @py_assert7 ** @py_assert9
        @py_assert12 = 10
        @py_assert14 = 3
        @py_assert16 = @py_assert12 ** @py_assert14
        @py_assert17 = 0.2
        @py_assert19 = 10
        @py_assert21 = 3
        @py_assert23 = @py_assert19 ** @py_assert21
        @py_assert24 = @py_assert5(@py_assert11, A=@py_assert16, b=@py_assert17, E=@py_assert23)
        @py_assert27 = 754.4574202941535
        @py_assert26 = @py_assert24 == @py_assert27
        if not @py_assert26:
            @py_format29 = @pytest_ar._call_reprcompare(('==', ), (@py_assert26,), ('%(py25)s\n{%(py25)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.ChemKin\n}.reaction_coeff\n}.mod_arr\n}((%(py8)s ** %(py10)s), A=(%(py13)s ** %(py15)s), b=%(py18)s, E=(%(py20)s ** %(py22)s))\n} == %(py28)s', ), (@py_assert24, @py_assert27)) % {'py0':@pytest_ar._saferepr(chemkin) if 'chemkin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chemkin) else 'chemkin',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19),  'py22':@pytest_ar._saferepr(@py_assert21),  'py25':@pytest_ar._saferepr(@py_assert24),  'py28':@pytest_ar._saferepr(@py_assert27)}
            @py_format31 = 'assert %(py30)s' % {'py30': @py_format29}
            raise AssertionError(@pytest_ar._format_explanation(@py_format31))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = @py_assert19 = @py_assert21 = @py_assert23 = @py_assert24 = @py_assert26 = @py_assert27 = None

    def test_Arrhenius_modified_argument_number(self):
        try:
            chemkin.ChemKin.reaction_coeff.mod_arr(10000, 1000, A=10000000, b=0.4, E=100)
        except TypeError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == TypeError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, TypeError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(TypeError) if 'TypeError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TypeError) else 'TypeError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_modified_type_A(self):
        try:
            chemkin.ChemKin.reaction_coeff.mod_arr(100, A='panama', b=0.4, E=1000)
        except TypeError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == TypeError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, TypeError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(TypeError) if 'TypeError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TypeError) else 'TypeError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_modified_type_b(self):
        try:
            chemkin.ChemKin.reaction_coeff.mod_arr(100, A=10000000, b='panama', E=1000)
        except TypeError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == TypeError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, TypeError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(TypeError) if 'TypeError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TypeError) else 'TypeError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_modified_type_E(self):
        try:
            chemkin.ChemKin.reaction_coeff.mod_arr(100, A=10000000, b=0.4, E='panama')
        except TypeError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == TypeError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, TypeError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(TypeError) if 'TypeError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TypeError) else 'TypeError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_modified_type_T(self):
        try:
            chemkin.ChemKin.reaction_coeff.mod_arr('panama', A=10000000, b=0.4, E=1000)
        except TypeError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == TypeError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, TypeError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(TypeError) if 'TypeError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TypeError) else 'TypeError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_modified_value_negative_A(self):
        try:
            chemkin.ChemKin.reaction_coeff.mod_arr(100, A=(-10000000), b=0.3, E=1000)
        except ValueError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_modified_value_negative_E(self):
        try:
            chemkin.ChemKin.reaction_coeff.mod_arr(100, A=10000000, b=0.3, E=(-1000))
        except ValueError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_modified_value_negative_T(self):
        try:
            chemkin.ChemKin.reaction_coeff.mod_arr((-100), A=10000000, b=0.3, E=1000)
        except ValueError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_flow_A(self):
        try:
            chemkin.ChemKin.reaction_coeff.mod_arr(100, A=(float('inf')), b=0.3, E=1000)
        except ValueError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_flow_b(self):
        try:
            chemkin.ChemKin.reaction_coeff.mod_arr(100, A=1000, b=(float('inf')), E=1000)
        except ValueError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_flow_E(self):
        try:
            chemkin.ChemKin.reaction_coeff.mod_arr(100, A=1000, b=0.3, E=(float('inf')))
        except ValueError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None

    def test_Arrhenius_flow_T(self):
        try:
            chemkin.ChemKin.reaction_coeff.mod_arr((float('inf')), A=100, b=0.3, E=1000)
        except ValueError as err:
            @py_assert2 = type(err)
            @py_assert4 = @py_assert2 == ValueError
            if not @py_assert4:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, ValueError)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py1':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(ValueError) if 'ValueError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ValueError) else 'ValueError'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert2 = @py_assert4 = None